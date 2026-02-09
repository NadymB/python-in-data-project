/* OPTIMIZED QUERIES (AFTER INDEX + PARTITION) */

-- Q1. Total revenue per month
EXPLAIN (ANALYZE, FORMAT JSON)
SELECT 
	DATE_TRUNC('month', order_date) AS month,
	SUM(total_amount)
FROM "order"
GROUP BY month;

-- Q2. Orders filtered by seller and date
EXPLAIN (ANALYZE, FORMAT JSON)
SELECT *
FROM "order"
WHERE seller_id = 10  
	AND order_date >= '2025-10-01' 
	AND order_date <= '2025-10-31';

-- Q3. Filter data in order_item by product_id
EXPLAIN (ANALYZE, FORMAT JSON)
SELECT *
FROM order_item
WHERE product_id = 100;

-- Q4. Find order with highest total_amount
EXPLAIN (ANALYZE, FORMAT JSON)
SELECT * 
FROM "order"
ORDER BY total_amount
LIMIT 1;

-- Q5. List products with highest quantity sold
EXPLAIN (ANALYZE, FORMAT JSON) 
SELECT product_id, SUM(quantity) AS qty_sold
FROM order_item
GROUP BY product_id
ORDER BY qty_sold ASC
LIMIT 1;

-- Q6. Revenue per Product per Month
EXPLAIN (ANALYZE, FORMAT JSON) 
SELECT 
	DATE_TRUNC('month', order_date) AS month,
	product_id,
	SUM(subtotal)
FROM order_item 
GROUP BY product_id, month;

-- Q7. Products Sold per Seller
EXPLAIN (ANALYZE, FORMAT JSON) 
SELECT 
	o.seller_id,
	it.product_id,
	SUM(it.quantity) AS qty
FROM "order" AS o
INNER JOIN order_item AS it ON o.order_id = it.order_id
GROUP BY o.seller_id, it.product_id
ORDER BY seller_id DESC;