<div align="center" >
  <h1><strong>Tiki Product Data Engineering Pipeline</strong></h1>
</div>

## Overview 
This project implements a full ETL (Extract – Transform – Load) pipeline for an E-Commerce OLTP system using Python + Faker to generate synthetic data: 
- Extracts fake raw data (CSV files)
- Transforms & cleans the data based on database schema
- Loads the cleaned data into a PostgreSQL database
- Includes data quality tests to ensure reliability before inserting into the database

## ERD 
<p align="center">
  <img src="assets/images/ecom-erd.svg" alt="E-Commerce ERD">
</p>

| Table | Column |
|-----:|-----------|
|     brand| brand_id, brand_name, country, created_at   |
|     category| category_id, category_name, parent_category_id, level, created_at|
|     seller| seller_id, seller_name, join_date, seller_type, rating, country    |
|     product| product_id, product_name, category_id, brand_id, seller_id, price, discount_price, stock_qty, rating, created_at, is_active       |
|     order | order_id, order_date, seller_id, status, total_amount, created_at       |
|     order_item| order_item_id, order_id, product_id, quantity, unit_price, subtotal     |
|     promotion| promotion_id, promotion_name, promotion_type, discount_type, discount_value, start_date, end_date       |
|     promotion_product| promotion_product_id, product_id, promotion_id, created_at       |

## ETL Pipeline
1. Extract:
- Generate fake E-Commerce data using Python + Faker
2. Transform:
- Clean and validate data using pandas
- Apply schema database
  - Check type of each column
  - Handle missing values
  - Enforce foreign key logic
  - Validate ranges (price, rating, level, dates)
3. Load:
- Load cleaned data into PostgreSQL

## Environment variable:
```
DB_HOST=your_host
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
DATA_PATH=./data
```

## Dependency Management (Poetry)
```
poetry install
poetry shell
```

## Conclusion 
This project delivers a reliable ETL pipeline for an E-Commerce system, from data generation and transformation to loading into PostgreSQL.
