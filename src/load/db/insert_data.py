import pandas as pd
from config.paths import PROCESSED_DATA_DIR
from psycopg2.extras import execute_values

def insert_data(db_connection, csv_path ,table_name, columns):
    # Read data from CSV
    df = pd.read_csv(csv_path)

    if table_name == "order":
        df = df.drop(columns=["order_bk"])

    if df.empty:
        return 

    # Convert list of dicts → list of tuples in correct column order
    values = [
        tuple(None if pd.isna(v) else v for v in row)
        for row in df[columns].to_numpy()
    ]

    # Build SQL query string dynamically
    col_str = ", ".join(columns)
    placeholders = ", ".join(["%s"] * len(columns))
    insert_query = f'''INSERT INTO "{table_name}" ({col_str}) VALUES ({placeholders})'''

    try:
        with db_connection.cursor() as cursor:
            cursor.executemany(insert_query, values)
        db_connection.commit()
        print(f"Inserted {len(values)} rows into {table_name}")
    except Exception as e:
        db_connection.rollback()
        print(f"Error inserting into {table_name}: {e}")
        raise


def load_dimension_tables(conn):

    insert_data(
        conn,
        PROCESSED_DATA_DIR / "brands_cleaned.csv",
        "brand",
        ["brand_name", "country", "created_at"]
    )

    insert_data(
        conn,
        PROCESSED_DATA_DIR / "categories_cleaned.csv",
        "category",
        ["category_name", "parent_category_id", "level", "created_at"]
    )

    insert_data(
        conn,
        PROCESSED_DATA_DIR / "sellers_cleaned.csv",
        "seller",
        ["seller_name", "join_date", "seller_type", "rating", "country"]
    )

    insert_data(
        conn,
        PROCESSED_DATA_DIR / "products_cleaned.csv",
        "product",
        [
            "product_name", "brand_id", "category_id",
            "seller_id", "price", "discount_price",
            "stock_qty", "rating", "created_at", "is_active"
        ]
    )

    insert_data(
        conn,
        PROCESSED_DATA_DIR / "promotions_cleaned.csv",
        "promotion",
        [
            "promotion_name", "promotion_type",
            "discount_type", "discount_value",
            "start_date", "end_date"
        ]
    )

    insert_data(
        conn,
        PROCESSED_DATA_DIR / "promotion_products_cleaned.csv",
        "promotion_product",
        ["promotion_id", "product_id", "created_at"]
    )

def load_fact_tables(db_connection):
    # columns for orders and order_items
    order_columns = [
        "order_date", "seller_id",
        "status", "total_amount", "created_at"
    ]
    order_item_columns = [ 
        "order_id", "order_date", "product_id",
        "quantity", "unit_price",
        "subtotal", "created_at"
    ]
    
    insert_data(
        db_connection,
        PROCESSED_DATA_DIR / "orders_cleaned.csv",
        "order",
        order_columns
    )

    insert_data(
        db_connection,
        PROCESSED_DATA_DIR / "order_items_cleaned.csv",
        "order_item",
        order_item_columns
    )