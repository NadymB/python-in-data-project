from src.extract.generate_data import generate_brand_fake_data, generate_category_product_fake_data , generate_seller_fake_data, generate_product_fake_data, generate_promotion_fake_data, generate_promotion_product_fake_data
from src.utils.constants import SELLER_TYPE, PROMOTION_TYPE, DISCOUNT_TYPE

def test_generate_brand_fake_data():
    data = generate_brand_fake_data(5)
    assert len(data) == 5
    for record in data:
        assert "brand_name" in record
        assert "country" in record
        assert "created_at" in record

def test_generate_category_product_fake_data():
    parent_ids = [1, 2, 3]
    data = generate_category_product_fake_data(10, parent_ids)
    assert len(data) == 10
    for record in data:
        assert "category_name" in record
        assert "level" in record
        assert "created_at" in record
        if record["level"] == 2:
            assert record["parent_category_id"] in parent_ids
        else:
            assert record["parent_category_id"] is None

def test_generate_seller_fake_data():
    data = generate_seller_fake_data(7)
    assert len(data) == 7
    for record in data:
        assert "seller_name" in record
        assert "join_date" in record
        assert "seller_type" in record
        assert record["seller_type"] in SELLER_TYPE
        assert "rating" in record
        assert 3 <= record["rating"] <= 5
        assert "country" in record
        assert "created_at" in record

def test_generate_product_fake_data():
    brand_ids = [1, 2, 3]
    category_ids = [1, 2, 3]
    seller_ids = [1, 2, 3]
    data = generate_product_fake_data(8, brand_ids, category_ids, seller_ids)
    assert len(data) == 8
    for record in data:
        assert "product_name" in record
        assert record["brand_id"] in brand_ids
        assert record["category_id"] in category_ids
        assert record["seller_id"] in seller_ids
        assert "price" in record
        assert 100000 <= record["price"] <= 50000000
        assert "discount_price" in record
        assert record["discount_price"] <= record["price"]
        assert "stock_qty" in record
        assert 0 <= record["stock_qty"] <= 500
        assert "rating" in record
        assert 3 <= record["rating"] <= 5
        assert "created_at" in record
        assert "is_active" in record
        assert isinstance(record["is_active"], bool)

def test_generate_promotion_fake_data():
    data = generate_promotion_fake_data(4)
    assert len(data) == 4
    for record in data:
        assert "promotion_name" in record
        assert "promotion_type" in record
        assert record["promotion_type"] in PROMOTION_TYPE
        assert "discount_type" in record
        assert record["discount_type"] in DISCOUNT_TYPE.values()
        assert "discount_value" in record
        if record["discount_type"] == DISCOUNT_TYPE[0]: # percentage
            assert 5 <= record["discount_value"] <= 50
        else: # fixed_amount
            assert 10000 <= record["discount_value"] <= 5000000
        assert "start_date" in record
        assert "end_date" in record

def test_generate_promotion_product_fake_data():
    promotion_ids = [1, 2, 3]
    product_ids = [1, 2, 3]
    data = generate_promotion_product_fake_data(6, promotion_ids, product_ids)
    assert len(data) == 6
    for record in data:
        assert record["promotion_id"] in promotion_ids
        assert record["product_id"] in product_ids
        assert "created_at" in record

if __name__ == "__main__":
    test_generate_brand_fake_data()
    test_generate_category_product_fake_data()
    test_generate_seller_fake_data()
    test_generate_product_fake_data()
    test_generate_promotion_fake_data()
    test_generate_promotion_product_fake_data()
    print("All tests passed!")