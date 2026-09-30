from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

import pandas as pd


SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

import data_quality
import generate_report
import load_data


class PipelineTests(unittest.TestCase):
    def test_quality_checks_report_missing_duplicates_and_invalid_values(self) -> None:
        frame = pd.DataFrame(
            {
                "InvoiceDate": ["2011-01-01 10:00", "invalid", "2011-01-01 10:00"],
                "Quantity": [2, -1, 2],
                "UnitPrice": [3.5, 0.0, 3.5],
                "CustomerID": [12345, None, 12345],
            }
        )
        output = mock_open()

        with patch.object(data_quality.pd, "read_csv", return_value=frame), \
             patch.object(data_quality.os, "makedirs"), \
             patch("builtins.open", output):
            result = data_quality.run_quality_checks()

        self.assertEqual(result["InvoiceDate"].isna().sum(), 1)
        report = "".join(call.args[0] for call in output().write.call_args_list)
        self.assertIn("Duplicate Rows: 1", report)
        self.assertIn("Negative Quantities: 1", report)
        self.assertIn("Zero or Negative Prices: 1", report)

    def test_kpi_report_excludes_cancellations_and_negative_quantities(self) -> None:
        frame = pd.DataFrame(
            {
                "InvoiceNo": ["100", "C101", "102", "103"],
                "Description": ["Widget", "Cancelled", "Return", "Gadget"],
                "Quantity": [2, 3, -1, 1],
                "UnitPrice": [10.0, 20.0, 15.0, 5.0],
                "InvoiceDate": ["2011-01-01", "2011-01-01", "2011-01-01", "2011-02-01"],
                "Country": ["United Kingdom", "United Kingdom", "France", "France"],
            }
        )
        output = mock_open()

        with patch.object(generate_report.pd, "read_csv", return_value=frame), \
             patch.object(generate_report.os, "makedirs"), \
             patch("builtins.open", output):
            cleaned, monthly, products, countries, top_countries = generate_report.generate_report()

        self.assertEqual(len(cleaned), 2)
        self.assertEqual(cleaned["Revenue"].sum(), 25.0)
        self.assertEqual(monthly.sum(), 25.0)
        self.assertEqual(products.index[0], "Widget")
        self.assertEqual(countries.index[0], "United Kingdom")
        self.assertEqual(len(top_countries), 2)

    def test_loader_cleans_rows_and_closes_the_database_connection(self) -> None:
        frame = pd.DataFrame(
            {
                "InvoiceNo": ["100", None],
                "StockCode": ["A", "B"],
                "Description": ["Widget", "Dropped"],
                "Quantity": [2, 1],
                "InvoiceDate": ["2011-01-01 10:00", "2011-01-01 11:00"],
                "UnitPrice": [3.5, 4.0],
                "CustomerID": [12345, 67890],
                "Country": ["United Kingdom", "France"],
            }
        )
        connection = MagicMock()
        cursor = MagicMock()
        connection.cursor.return_value = cursor
        connection.is_connected.return_value = True

        with patch.object(load_data.pd, "read_csv", return_value=frame), \
             patch.object(load_data.mysql.connector, "connect", return_value=connection):
            cleaned = load_data.load_data()

        self.assertEqual(len(cleaned), 1)
        self.assertEqual(cursor.execute.call_count, 1)
        connection.commit.assert_called_once()
        cursor.close.assert_called_once()
        connection.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
