CREATE OR REPLACE FUNCTION seller_performance_report(
	start_date DATE,
	end_date DATE,
	category_id INT,
	brand_id INT
)
RETURNS TABLE (
	seller_id INT, 
	seller_name TEXT,
	total_orders BIGINT,
	total_quantity BIGINT,
	total_revenue BIGINT
) 
LANGUAGE sql
AS $$
	SELECT 
		s.seller_id,
		s.seller_name,
		count(o.order_id) AS total_orders,
		sum(oi.quantity) AS total_quantity,
		sum(oi.subtotal) AS total_revenue
	FROM "order" AS o
	JOIN seller AS s ON o.seller_id = s.seller_id 
	JOIN order_item AS oi ON o.order_id = oi.order_id
	JOIN product AS p ON oi.product_id = p.product_id
	WHERE o.order_date >= start_date AND o.order_date <= end_date
	AND p.category_id = category_id AND p.brand_id = brand_id 
	GROUP BY s.seller_id, s.seller_name
	ORDER BY total_revenue DESC
$$;

EXPLAIN (ANALYZE, FORMAT JSON)
SELECT * FROM seller_performance_report('2025-09-01', '2025-10-01', 10, 5);