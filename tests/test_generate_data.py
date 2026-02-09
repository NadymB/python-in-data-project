from src.extract.generate_data import generate_brand_fake_data, generate_category_product_fake_data , generate_seller_fake_data, generate_product_fake_data, generate_promotion_fake_data, generate_promotion_product_fake_data
from src.utils.constants import SELLER_TYPE, PROMOTION_TYPE, DISCOUNT_TYPE
from src.extract.generate_data import generate_orders_and_order_items_fake_data
from datetime import datetime
from src.utils.constants import ORDER_STATUS
import pandas as pd 

products_dump = {
    1: [
        {"product_id":1, "discount_price":100},
        {"product_id":2, "discount_price":200},
        {"product_id":3, "discount_price":300},
    ],
    2: [
        {"product_id":4, "discount_price":400},
        {"product_id":5, "discount_price":500},
        {"product_id":6, "discount_price":600},
    ]
}

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

def test_generate_orders_and_order_items_fake_data():
    # Test right length orders and order items
    orders, order_items = generate_orders_and_order_items_fake_data(100, products_dump)
    assert len(orders) == 100
    assert len(order_items) >= 200

    # Test each order has 2 - 4 items 
    order_count = {}

    for it in order_items:
        order_count.setdefault(it["order_id"], 0)
        order_count[it["order_id"]] += 1

    for cnt in order_count.values():
        assert 2 <= cnt <= 4

    # Test total_amount = sum(subtotal)
    subtotal_map = {}

    for it in order_items:
        subtotal_map.setdefault(it["order_id"], 0)
        subtotal_map[it["order_id"]] += it["subtotal"]

    for o in orders: 
        assert round(o["total_amount"], 2) == round(subtotal_map[o["order_bk"]], 2)
    
    # Test each product must belong to same seller_id as order
    product_seller = {}

    for seller_id, products in products_dump.items():
        for p in products:
            product_seller[p["product_id"]] = seller_id

    order_seller = {
        o["order_bk"]: o["seller_id"] for o in orders 
    }

    for it in order_items:
        assert product_seller[it["product_id"]] == order_seller[it["order_id"]]

    # Test order date ranges:
    start = datetime(2025, 8, 1).date()
    end = datetime(2025, 10, 31).date()
    
    for o in orders:
        order_date = o["order_date"]
        if isinstance(order_date, datetime):
            order_date = order_date.date()

        assert start <= order_date <= end

    for it in order_items:
        order_date = it["order_date"]
        if isinstance(order_date, datetime):
            order_date = order_date.date()

        assert start <= order_date <= end

    # Test status validity
    for o in orders:
        assert o["status"] in list(ORDER_STATUS.values())

if __name__ == "__main__":
    test_generate_brand_fake_data()
    test_generate_category_product_fake_data()
    test_generate_seller_fake_data()
    test_generate_product_fake_data()
    test_generate_promotion_fake_data()
    test_generate_promotion_product_fake_data()
    test_generate_orders_and_order_items_fake_data()
    print("All tests passed!")