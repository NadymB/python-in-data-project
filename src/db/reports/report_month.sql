CREATE OR REPLACE FUNCTION report_month(
	start_date DATE,
	end_date DATE
)
RETURNS TABLE (
	month DATE,
	total_orders BIGINT,
	total_quantity BIGINT,
	total_revenue NUMERIC
) 
LANGUAGE sql
AS $$ 
	SELECT 
		DATE_TRUNC('month', o.order_date)::DATE AS month,
		count(DISTINCT o.order_id) AS total_orders,
		sum(oi.quantity) AS quantity,
		sum(oi.subtotal) AS total_revenue
	FROM "order" AS o
	JOIN "order_item" AS oi ON o.order_id = oi.order_id
	WHERE o.order_date >= start_date AND o.order_date <= end_date
	GROUP BY 1
	ORDER BY 1;
$$;

EXPLAIN (ANALYZE, FORMAT JSON)
SELECT * FROM report_month('2025-08-01', '2025-10-31');