from faker import Faker
from datetime import timedelta

from src.utils.format_date import format_date
from src.utils.constants import SELLER_TYPE, PROMOTION_TYPE, DISCOUNT_TYPE
from datetime import datetime
import random
import pandas as pd

fake = Faker("vi_VN")

def generate_brand_fake_data(num_records):
    brand_data = []
    for _ in range(num_records):
        brand = {
            "brand_name": fake.company(),
            "country": fake.country(),
            "created_at": format_date(fake.date_time_this_decade())
        }
        brand_data.append(brand)
    return brand_data

def generate_category_product_fake_data(num_records, parent_category_ids):
    category_data = []
    for _ in range(num_records):
        # 70% chance to be a sub-category
        if parent_category_ids and random.random() < 0.7:
            parent_id = random.choice(parent_category_ids)
            level = 2
        else:
            parent_id = None
            level = 1

        category = {
            "category_name": fake.word().title(),
            "parent_category_id": parent_id,
            "level": level,
            "created_at": format_date(fake.date_time_this_year())
        }
        category_data.append(category)
    return category_data

def generate_seller_fake_data(num_records):
    seller_data = []
    for _ in range(num_records):
        seller = {
            "seller_name": fake.company(),
            "join_date": fake.date_between(start_date='-3y', end_date='today'),
            "seller_type": random.choice(SELLER_TYPE),
            "rating": round(random.uniform(3, 5), 1),
            "country": "Vietnam",
            "created_at": format_date(fake.date_time_this_year())
        }
        seller_data.append(seller)
    return seller_data

def generate_product_fake_data(num_records, brand_ids, category_ids, seller_ids):
    product_data = []
    for _ in range(num_records):
        price = round(random.uniform(100000, 50000000), 2)
        discount_price = round(price * random.uniform(0.7, 1.0), 2)
        product = {
            "product_name": fake.catch_phrase(),
            "brand_id": random.choice(brand_ids),
            "category_id": random.choice(category_ids),
            "seller_id": random.choice(seller_ids),
            "price": price,
            "discount_price": discount_price,
            "stock_qty": random.randint(0, 500),
            "rating": round(random.uniform(3, 5), 1),
            "created_at": format_date(fake.date_time_this_year()),
            "is_active": fake.boolean(chance_of_getting_true=90)
        }
        product_data.append(product)
    return product_data

def generate_promotion_fake_data(num_records):
    promotion_data = []
    for _ in range(num_records):
        discount_type = random.choice(list(DISCOUNT_TYPE.values()))

        if discount_type == DISCOUNT_TYPE[0]: # percentage
            discount_value = round(random.uniform(5, 50), 2)
        else:
            discount_value = round(random.uniform(10000, 5000000), 2)

        start_date = fake.date_between(start_date='-1y', end_date='today')
        end_date = start_date + timedelta(days=random.randint(30, 50))
        promotion = {
            "promotion_name": fake.catch_phrase(),
            "promotion_type": random.choice(PROMOTION_TYPE),
            "discount_type": discount_type,
            "discount_value": discount_value,
            "start_date": format_date(start_date),
            "end_date": format_date(end_date)
        }
        promotion_data.append(promotion)
    return promotion_data

def generate_promotion_product_fake_data(num_records, promotion_ids, product_ids):
    promotion_product_data = []
    for _ in range(num_records):
        promotion_product = {
            "promotion_id": random.choice(promotion_ids),
            "product_id": random.choice(product_ids),
            "created_at": format_date(fake.date_time_this_year())
        }
        promotion_product_data.append(promotion_product)
    return promotion_product_data

def random_status():
    r = random.random()
    if r < 0.8:
        return random.choice(["PAID", "DELIVERED"])
    elif r < 0.9:
        return random.choice(["CANCELLED", "RETURNED"])
    else:
        return random.choice(["PLACED", "SHIPPED"])

def generate_orders_and_order_items_fake_data(num_orders, seller_products):
    orders = []
    order_items = []

    order_id = 1
    for _ in range(num_orders):

        seller_id = random.choice(list(seller_products.keys()))
        available_products = seller_products[seller_id]

        if len(available_products) < 2:
            continue

        k = min(len(available_products), random.randint(2, 4))
        # Faking 2-4 products per order
        products = random.sample(available_products, k=k)

        # Faker status
        status = random_status()

        # Faker order date
        start_dt = datetime(2025, 8, 1)
        end_dt   = datetime(2025, 10, 31)

        order_date = fake.date_between(
            start_date=start_dt,
            end_date=end_dt
        )

        total_amount = 0

        for p in products:

            qty = random.randint(1, 5)
            unit_price = float(p["discount_price"])
            subtotal = round(qty * unit_price, 2)

            order_items.append({
                "order_id": order_id,
                "product_id": p["product_id"],
                "order_date": order_date,
                "quantity": qty,
                "unit_price": unit_price,
                "subtotal": subtotal,
                "created_at": order_date
            })

            total_amount += subtotal

        orders.append({
            "order_bk": order_id,
            "order_date": order_date,
            "seller_id": seller_id,
            "status": status,
            "total_amount": round(total_amount, 2),
            "created_at": order_date
        })
        order_id += 1

    return orders, order_items