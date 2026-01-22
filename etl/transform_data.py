from src.transform.clean_data import (
    clean_brand_data,
    clean_category_data,
    clean_seller_data,
    clean_product_data,
    clean_promotion_data,
    clean_promotion_product_data
)

def main():
    clean_brand_data()
    clean_category_data()
    clean_seller_data()
    clean_product_data()
    clean_promotion_data()
    clean_promotion_product_data()

if __name__ == "__main__":
    main()