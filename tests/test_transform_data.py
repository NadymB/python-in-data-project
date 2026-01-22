import pandas as pd
from pandas.api.types import is_string_dtype
from config.paths import PROCESSED_DATA_DIR

def test_category_schema():
    df = pd.read_csv(PROCESSED_DATA_DIR / "categories_cleaned.csv")

    # ===== Column existence =====
    expected_cols = {
        "category_name",
        "parent_category_id",
        "level",
        "created_at",
    }
    assert expected_cols.issubset(df.columns)

    # ===== Type checks =====
    assert is_string_dtype(df["category_name"])
    assert df["level"].dropna().isin([1, 2]).all()

    # parent_category_id: INT or NULL
    assert df["parent_category_id"].dropna().apply(lambda x: x % 1 == 0).all()

    # created_at must be valid date
    pd.to_datetime(df["created_at"], errors="raise")

def test_category_parent_fk_logic():
    df = pd.read_csv(PROCESSED_DATA_DIR / "categories_cleaned.csv")

    category_ids = set(range(1, len(df) + 1))

    invalid_parent = df[
        df["parent_category_id"]
        .dropna()
        .astype(int)
    ]

    assert invalid_parent.empty

def test_brand_schema():
    df = pd.read_csv(PROCESSED_DATA_DIR / "brands_cleaned.csv")

    assert df["brand_name"].notna().all()
    assert df["created_at"].notna().all()

    pd.to_datetime(df["created_at"], errors="raise")

def test_seller_constraints():
    df = pd.read_csv(PROCESSED_DATA_DIR / "sellers_cleaned.csv")

    assert df["seller_type"].isin(["Official", "Marketplace"]).all()
    assert df["rating"].between(0, 5).all()

def test_product_constraints():
    df = pd.read_csv(PROCESSED_DATA_DIR / "products_cleaned.csv")

    assert (df["price"] >= 0).all()
    assert (df["discount_price"] <= df["price"]).all()
    assert (df["stock_qty"] >= 0).all()
    assert df["rating"].between(0, 5).all()

def test_product_fk_not_null():
    df = pd.read_csv(PROCESSED_DATA_DIR / "products_cleaned.csv")

    for col in ["brand_id", "category_id", "seller_id"]:
        assert df[col].notna().all()
        assert df[col].apply(lambda x: x % 1 == 0).all()

def test_promotion_dates():
    df = pd.read_csv(PROCESSED_DATA_DIR / "promotions_cleaned.csv")

    start = pd.to_datetime(df["start_date"])
    end = pd.to_datetime(df["end_date"])

    assert (end > start).all()

def test_promotion_product_ids():
    df = pd.read_csv(PROCESSED_DATA_DIR / "promotion_products_cleaned.csv")

    assert df["promotion_id"].apply(lambda x: x % 1 == 0).all()
    assert df["product_id"].apply(lambda x: x % 1 == 0).all()

