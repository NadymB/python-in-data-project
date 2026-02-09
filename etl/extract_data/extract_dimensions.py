from src.extract.generate_data import (
    generate_brand_fake_data,
    generate_category_product_fake_data,
    generate_seller_fake_data,
    generate_product_fake_data,
    generate_promotion_fake_data,
    generate_promotion_product_fake_data,
)
from config.paths import RAW_DATA_DIR
from src.load.file.write_csv import write_csv

def main():
    # --------------------------
    # 1. Generate Brands
    # --------------------------
    brands = generate_brand_fake_data(20)
    write_csv(RAW_DATA_DIR / "brands.csv", brands)
    brand_ids = list(range(1, len(brands)+1))

    # --------------------------
    # 2. Generate Categories
    # --------------------------
    # First generate 5 main categories (level 1)
    main_categories = generate_category_product_fake_data(5, [])
    main_category_ids = list(range(1, len(main_categories)+1))

    # Then generate 10 sub-categories (level 2), parent is random from main_categories
    sub_categories = generate_category_product_fake_data(10, main_category_ids)
    categories = main_categories + sub_categories
    write_csv(RAW_DATA_DIR / "categories.csv", categories)
    category_ids = list(range(1, len(categories)+1))

    # --------------------------
    # 3. Generate Sellers
    # --------------------------
    sellers = generate_seller_fake_data(25)
    write_csv(RAW_DATA_DIR / "sellers.csv", sellers)
    seller_ids = list(range(1, len(sellers)+1))

    # --------------------------
    # 4️⃣ Generate Products
    # --------------------------
    products = generate_product_fake_data(
        num_records=2000,
        brand_ids=brand_ids,
        category_ids=category_ids,
        seller_ids=seller_ids
    )
    write_csv(RAW_DATA_DIR / "products.csv", products)
    product_ids = list(range(1, len(products)+1))

    # --------------------------
    # 5. Generate Promotions
    # --------------------------
    promotions = generate_promotion_fake_data(10)
    write_csv(RAW_DATA_DIR / "promotions.csv", promotions)
    promotion_ids = list(range(1, len(promotions)+1))

    # --------------------------
    # 6. Generate Promotion_Product mappings
    # --------------------------
    promotion_products = generate_promotion_product_fake_data(
        num_records=100,
        promotion_ids=promotion_ids,
        product_ids=product_ids
    )
    write_csv(RAW_DATA_DIR / "promotion_products.csv", promotion_products)

if __name__ == "__main__":
    main()