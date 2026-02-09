CREATE OR REPLACE FUNCTION report_daily(
	start_date DATE,
	end_date DATE,
	product_list INT[]
)
RETURNS TABLE (
	report_date DATE,
	total_orders BIGINT,
	total_quantity BIGINT,
	total_revenue BIGINT
)
LANGUAGE sql
AS $$
	SELECT 
		o.order_date::DATE AS report_date,
		count(DISTINCT o.order_id) AS total_orders,
		sum(oi.quantity) AS total_quantity,
		sum(oi.subtotal) AS total_revenue
	FROM "order" AS o
	JOIN "order_item" AS oi ON o.order_id = oi.order_id 
	WHERE o.order_date >= start_date AND o.order_date <= end_date
	AND oi.product_id = ANY(product_list) 
	GROUP BY 1
	ORDER BY 1;
$$;

EXPLAIN (ANALYZE, FORMAT JSON)
SELECT * FROM report_daily('2025-08-01', '2025-10-31', ARRAY[10, 30, 40]);
