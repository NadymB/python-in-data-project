from src.transform.clean_data import (
    clean_orders_data,
    clean_order_items_data
)

def main():
    clean_orders_data()
    clean_order_items_data()

if __name__ == "__main__":
    main()