import pandas as pd
from config.paths import RAW_DATA_DIR, PROCESSED_DATA_DIR
from src.utils.constants import PROMOTION_TYPE, SELLER_TYPE
from src.load.file.saved_csv import save_cleaned

def clean_brand_data():
    input_file = RAW_DATA_DIR / "brands.csv"
    output_file = PROCESSED_DATA_DIR / "brands_cleaned.csv"

    # Read the raw brand data
    df = pd.read_csv(input_file)

    # CLEANING BRAND DATA 
    df['brand_name'] = df['brand_name'].str.strip()
    df = df[df['brand_name'].str.len() > 100]
    df['country'] = df['country'].str.strip()
    df = df[df['country'].str.len() > 50]
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce').dt.strftime('%Y-%m-%d')

    # Remove rows with missing brand_name or created_at
    df = df.dropna(subset=['brand_name', 'created_at'])

    # Remove duplicates
    df = df.drop_duplicates(subset=['brand_name', 'country', 'created_at'])

    # Save the cleaned data
    save_cleaned(df, output_file)

def clean_category_data():
    input_file = RAW_DATA_DIR / "categories.csv"
    output_file = PROCESSED_DATA_DIR / "categories_cleaned.csv"

    # Read the raw category data
    df = pd.read_csv(input_file)

    # CLEANING CATEGORY DATA
    df['category_name'] = df['category_name'].str.strip()
    df = df[df['category_name'].str.len() > 100]
    df['level'] = pd.to_numeric(df['level'], errors='coerce')
    df = df[df['level'].isin([1, 2])]
    df['parent_category_id'] = pd.to_numeric(
        df['parent_category_id'], errors='coerce'
    ).astype('Int64')

    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce').dt.strftime('%Y-%m-%d')

    # Remove any rows with missing category names or created_at
    df = df.dropna(subset=['category_name', 'created_at'])

    # Remove duplicates
    df = df.drop_duplicates(subset=['category_name', 'level', 'parent_category_id', 'created_at'])

    # Save the cleaned data
    save_cleaned(df, output_file)

def clean_seller_data():
    input_file = RAW_DATA_DIR / "sellers.csv"
    output_file = PROCESSED_DATA_DIR / "sellers_cleaned.csv"

    # Read the raw seller data
    df = pd.read_csv(input_file)

    # CLEANING SELLER DATA
    df['seller_name'] = df['seller_name'].str.strip()
    df = df[df['seller_name'].str.len() > 150]

    df['seller_type'] = df['seller_type'].str.strip()
    df = df[df['seller_type'].str.len() > 50]
    df = df[df['seller_type'].isin(SELLER_TYPE)]

    df['rating'] = df['rating'].astype(float)
    df = df[(df['rating'] >= 3) & (df['rating'] <= 5)] 

    df['country'] = df['country'].str.strip()
    df = df[df['country'].str.len() > 50]

    df['join_date'] = pd.to_datetime(df['join_date'], errors='coerce').dt.strftime('%Y-%m-%d')
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce').dt.strftime('%Y-%m-%d')    

    # Remove rows with missing seller_name or created_at
    df = df.dropna(subset=['seller_name', 'join_date', 'created_at'])

    # Remove duplicates
    df = df.drop_duplicates(['seller_name', 'join_date', 'seller_type', 'rating', 'country', 'created_at'])

    # Save the cleaned data
    save_cleaned(df, output_file)

def clean_product_data():
    input_file = RAW_DATA_DIR / "products.csv"
    output_file = PROCESSED_DATA_DIR / "products_cleaned.csv"

    # Read the raw product data
    df = pd.read_csv(input_file)

    # CLEANING PRODUCT DATA
    df['product_name'] = df['product_name'].str.strip()
    df = df[df['product_name'].str.len() > 200]

    df['price'] = df['price'].astype(float).round(2)
    df['discount_price'] = df['discount_price'].astype(float).round(2)
    df = df[df['price'] >= 0]
    df = df[df['discount_price'] <= df['price']]

    df['stock_qty'] = (
        pd.to_numeric(df['stock_qty'], errors='coerce')
        .astype('Int64')
    )
    df['rating'] = df['rating'].astype(float)
    df = df[(df['rating'] >= 3) & (df['rating'] <= 5)]

    df['brand_id'] = (
        pd.to_numeric(df['brand_id'], errors='coerce')
        .astype('Int64')
    )
    df['category_id'] = (
        pd.to_numeric(df['category_id'], errors='coerce')
        .astype('Int64')
    )
    df['seller_id'] = (
        pd.to_numeric(df['seller_id'], errors='coerce')
        .astype('Int64')
    )

    df['is_active'] = df['is_active'].astype(bool)

    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce').dt.strftime('%Y-%m-%d')

    # Remove rows with missing product_name or created_at
    df = df.dropna(subset=['product_name', 'brand_id', 'category_id', 'seller_id', 'created_at'])

    # Remove duplicates
    df = df.drop_duplicates(subset=['product_name', 'brand_id', 'category_id', 'seller_id', 'created_at'])

    # Save the cleaned data
    save_cleaned(df, output_file)

def clean_promotion_data():
    input_file = RAW_DATA_DIR / "promotions.csv"
    output_file = PROCESSED_DATA_DIR / "promotions_cleaned.csv"

    # Read the raw promotion data
    df = pd.read_csv(input_file)

    # CLEANING PROMOTION DATA
    df['promotion_name'] = df['promotion_name'].str.strip()
    df = df[df['promotion_name'].str.len() > 100]

    df['promotion_type'] = df['promotion_type'].str.strip().str.lower()
    df = df[df['promotion_type'].str.len() > 50]
    df = df[df['promotion_type'].isin(PROMOTION_TYPE)]

    def normalize_discount(row):
        if row["discount_type"] == "percentage":
            return min(max(row["discount_value"], 0), 100)
        return max(row["discount_value"], 0)

    df["discount_value"] = df.apply(normalize_discount, axis=1).round(2)

    df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce')
    df['end_date'] = pd.to_datetime(df['end_date'], errors='coerce')

    df = df[df['end_date'] >= df['start_date']]

    df['start_date'] = df['start_date'].dt.strftime('%Y-%m-%d')
    df['end_date'] = df['end_date'].dt.strftime('%Y-%m-%d')

    # Remove rows with missing promotion_name, start_date, or end_date
    df = df.dropna(subset=['promotion_name', 'start_date', 'end_date'])

    # Remove duplicates
    df = df.drop_duplicates(['promotion_name', 'promotion_type', 'start_date', 'end_date'])

    # Save the cleaned data
    save_cleaned(df, output_file)

def clean_promotion_product_data():
    input_file = RAW_DATA_DIR / "promotion_products.csv"
    output_file = PROCESSED_DATA_DIR / "promotion_products_cleaned.csv"

    # Read the raw promotion-product mapping data
    df = pd.read_csv(input_file)

    # CLEANING PROMOTION-PRODUCT DATA
    df['promotion_id'] = (
        pd.to_numeric(df['promotion_id'], errors='coerce')
        .astype('Int64')
    )
    df['product_id'] = (
        pd.to_numeric(df['product_id'], errors='coerce')
        .astype('Int64')
    )

    # Remove rows with missing promotion_id or product_id
    df = df.dropna(subset=['promotion_id', 'product_id'])

    # Remove duplicates
    df = df.drop_duplicates(['promotion_id', 'product_id'])

    # Save the cleaned data
    save_cleaned(df, output_file)
