import os
import pandas as pd
import mysql.connector
from mysql.connector import Error

# 1️⃣ Read CSV
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR, "data", "dataset.csv")

df = pd.read_csv(file_path, encoding="ISO-8859-1")
print("Original shape:", df.shape)

# 2️⃣ Basic Cleaning

# Convert InvoiceDate to datetime
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")

# Drop rows with missing essential values
df = df.dropna(subset=["InvoiceNo", "StockCode", "Quantity", "UnitPrice"])

print("After cleaning shape:", df.shape)

# 3️⃣ Connect to MySQL
connection = None
cursor = None
try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # you said no password
        database="sales_db"
    )

    cursor = connection.cursor()

    # 4️⃣ Insert Data
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
            int(row["CustomerID"]) if pd.notna(row["CustomerID"]) and str(
                row["CustomerID"]) != "" else None,
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
