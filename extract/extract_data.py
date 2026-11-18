
import pandas as pd
from sqlalchemy import create_engine, URL
from dotenv import load_dotenv
import os

load_dotenv()

# Daftar tabel staging yang akan diekstrak
STAGING_TABLES = [
    "stg_customers",
    "stg_products",
    "stg_orders",
    "stg_order_items",
    "stg_payments",
    "stg_shipments",
    "stg_returns",
    "stg_customer_reviews",
    "stg_marketing_campaigns"
]


def get_engine():
    connection_url = URL.create(
        drivername="mysql+mysqlconnector",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD", ""),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 3306)),
        database=os.getenv("DB_NAME")
    )

    return create_engine(connection_url)


def extract_table(engine, table_name):
    query = f"SELECT * FROM `{table_name}`"

    df = pd.read_sql_query(query, engine)

    print(f"Berhasil mengambil: {table_name}")
    print(f"Jumlah baris: {len(df):,}")
    print(f"Jumlah kolom: {len(df.columns)}")
    print("-" * 40)

    return df


def extract_all_tables():
    engine = get_engine()
    extracted_data = {}

    try:
        print("MEMULAI PROSES EXTRACT\n")

        for table_name in STAGING_TABLES:
            df = extract_table(engine, table_name)
            extracted_data[table_name] = df

        print("PROSES EXTRACT SELESAI")
        return extracted_data

    finally:
        engine.dispose()
