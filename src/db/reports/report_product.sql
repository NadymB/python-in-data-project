CREATE OR REPLACE FUNCTION report_product(
	start_date DATE,
	end_date DATE,
	seller_list INT[],
	p_top_n INT DEFAULT 3
)
RETURNS TABLE (
	brand_id INT,
	brand_name TEXT,
	product_id INT,
	product_name TEXT,
	total_quantity BIGINT,
	total_revenue NUMERIC
) 
LANGUAGE sql
AS $$
	SELECT 
		brand_id,
		brand_name,
		product_id,
		product_name,
		total_quantity,
		total_revenue
	FROM (
		SELECT 
				b.brand_id,
				b.brand_name,
				p.product_id,
				p.product_name,
				sum(oi.quantity) AS total_quantity,
				sum(oi.subtotal) AS total_revenue,
				DENSE_RANK() OVER(PARTITION BY b.brand_id ORDER BY sum(oi.quantity) DESC) AS rank_brand
			FROM "order" AS o
			JOIN order_item AS oi ON o.order_id = oi.order_id
			JOIN product AS p ON oi.product_id = p.product_id 
			JOIN brand AS b ON p.brand_id = b.brand_id
			WHERE o.order_date >= start_date AND o.order_date <= end_date
				AND (
					seller_list IS NULL OR
					o.seller_id = ANY(seller_list)
				)
			GROUP BY b.brand_id, b.brand_name, p.product_id, p.product_name
	) t
	WHERE rank_brand <= p_top_n;
$$;

EXPLAIN (ANALYZE, FORMAT JSON)
SELECT * FROM report_product('2025-08-01', '2025-10-31', ARRAY[10, 18, 20]);