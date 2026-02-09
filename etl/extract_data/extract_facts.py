from src.db.config import load_config
from src.db.connect import connect
from src.load.file.write_csv import write_csv
from src.load.db.fetch_data import get_products_by_seller
from config.paths import RAW_DATA_DIR
from src.extract.generate_data import generate_orders_and_order_items_fake_data

def main():
    # --------------------------
    # Generate Orders and Order Items 
    # --------------------------    
    try:
        with connect(load_config()) as conn:
            products = get_products_by_seller(conn)
            orders, order_items = generate_orders_and_order_items_fake_data(2500000, products)
            write_csv(RAW_DATA_DIR / "orders.csv", orders)
            write_csv(RAW_DATA_DIR / "order_items.csv", order_items)
    except(Exception) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

