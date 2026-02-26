import os
import pandas as pd
import mysql.connector
from mysql.connector import Error


def load_data():
    """Load CSV, clean it, insert into MySQL, and return cleaned DataFrame."""

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(BASE_DIR, "data", "dataset.csv")

    # Load CSV
    df = pd.read_csv(file_path, encoding="ISO-8859-1")
    print("Original shape:", df.shape)

    # Basic cleaning
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    df = df.dropna(subset=["InvoiceNo", "StockCode", "Quantity", "UnitPrice"])
    print("After cleaning shape:", df.shape)

    # Insert into MySQL
    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # no password
            database="sales_db"
        )

        cursor = connection.cursor()

        insert_query = """
        INSERT INTO sales (
            invoice_no,
            stock_code,
            description,
            quantity,
            invoice_date,
            unit_price,
            customer_id,
            country
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        for _, row in df.iterrows():
            cursor.execute(insert_query, (
                str(row["InvoiceNo"]),
                str(row["StockCode"]),
                str(row["Description"]),
                int(row["Quantity"]),
                pd.Timestamp(row["InvoiceDate"]).strftime("%Y-%m-%d %H:%M:%S"),
                float(row["UnitPrice"]),
                int(row["CustomerID"]) if pd.notna(row["CustomerID"]) and str(row["CustomerID"]).strip() != "" else None,
                str(row["Country"])
            ))

        connection.commit()
        print("Data inserted successfully.")

    except Error as e:
        print("Error:", e)

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("MySQL connection closed.")

    return df
