/*===================================================================
    An E-Commerce OLTP System Schema 
===================================================================*/

-- Creating the data model
DROP DATABASE IF EXISTS ecommerce;

CREATE DATABASE ecommerce;

-- Create the structure of various tables in the ecommerce database
-- Table: brand
DROP TABLE IF EXISTS brand;
CREATE TABLE brand (
    brand_id SERIAL PRIMARY KEY, 
    brand_name VARCHAR(100),
    country VARCHAR(50),
    created_at TIMESTAMP
);

-- Table: Category
DROP TABLE IF EXISTS category;
CREATE TABLE category (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100),
    parent_category_id INT REFERENCES category(category_id),
    level SMALLINT CHECK(level IN (1, 2)),
    created_at TIMESTAMP
);

-- Table: Seller
DROP TABLE IF EXISTS seller;
CREATE TABLE seller (
    seller_id SERIAL PRIMARY KEY,
    seller_name VARCHAR(150),
    join_date DATE,
    seller_type VARCHAR(50) CHECK(seller_type IN ('Official', 'Marketplace')),
    rating DECIMAL(2,1) CHECK(rating BETWEEN 0 AND 5),
    country VARCHAR(50)
);

-- Table: Product
DROP TABLE IF EXISTS product;
CREATE TABLE product (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(200),
    category_id INT REFERENCES category(category_id),
    brand_id INT REFERENCES brand(brand_id),
    seller_id INT REFERENCES seller(seller_id),
    price DECIMAL(12, 2) CHECK(price >= 0),
    discount_price DECIMAL(12, 2) CHECK(discount_price <= price),
    stock_qty INT CHECK(stock_qty >= 0),
    rating FLOAT CHECK(rating BETWEEN 0 AND 5),
    created_at TIMESTAMP, 
    is_active BOOLEAN
);

-- Table: Order
DROP TABLE IF EXISTS order;
CREATE TABLE "order" (
    order_id SERIAL PRIMARY KEY,
    order_date DATE,
    seller_id INT REFERENCES seller(seller_id),
    status VARCHAR(20) CHECK(status IN('PLACED', 'PAID', 'SHIPPED', 'DELIVERED', 'CANCELLED', 'RETURNED')),
    total_amount DECIMAL(12, 2) CHECK(total_amount >= 0),
    created_at DATE
);

-- Table: Order_Item
DROP TABLE IF EXISTS order_item;
CREATE TABLE order_item (
    order_item_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES "order"(order_id),
    product_id INT REFERENCES product(product_id),
    order_date DATE,
    quantity INT CHECK(quantity > 0),
    unit_price DECIMAL(12, 2) CHECK(unit_price >= 0),
    subtotal DECIMAL(12, 2) CHECK(subtotal >= 0),
    created_at DATE
);

-- Table: Promotion
DROP TABLE IF EXISTS promotion;
CREATE TABLE promotion (
    promotion_id SERIAL PRIMARY KEY,
    promotion_name VARCHAR(100),
    promotion_type VARCHAR(50) CHECK(promotion_type IN ('product', 'category', 'seller', 'flash_sale', 'other')),
    discount_type VARCHAR(20) CHECK(discount_type IN ('percentage', 'fixed_amount')),
    discount_value NUMERIC(12, 2) CHECK(discount_value >= 0),
    start_date DATE,
    end_date DATE CHECK(end_date > start_date)
);

-- Table: Promotion_Product
DROP TABLE IF EXISTS promotion_product;
CREATE TABLE promotion_product (
    promotion_product_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES product(product_id),
    promotion_id INT REFERENCES promotion(promotion_id),
    created_at TIMESTAMP
);

