CREATE OR REPLACE FUNCTION order_status_summary(
	start_date DATE,
	end_date DATE,
	seller_list INT[] DEFAULT NULL,
	category_list INT[] DEFAULT NULL
)
RETURNS TABLE (
	status TEXT, 
	total_orders BIGINT,
	total_revenue NUMERIC
)
LANGUAGE sql
AS $$
	SELECT 
		o.status,
		count(DISTINCT o.order_id) AS total_orders,
		sum(oi.subtotal) AS total_revenue
	FROM "order" AS o
	JOIN order_item AS oi ON o.order_id = oi.order_id
	JOIN product AS p ON oi.product_id = p.product_id
	WHERE o.order_date >= start_date AND o.order_date <= end_date 
		AND (
			seller_list IS NULL OR 
			o.seller_id = ANY(seller_list)
		) 
		AND (
			category_list IS NULL OR 
			p.category_id = ANY(category_list)
		)
	GROUP BY o.status
	ORDER BY total_orders DESC;
$$;

EXPLAIN (ANALYZE, FORMAT JSON)
SELECT * FROM order_status_summary('2025-08-01', '2025-10-31', ARRAY[15, 32, 44]);