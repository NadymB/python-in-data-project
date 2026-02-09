-- Create index on product_id column in order_item table
CREATE INDEX index_order_item_product 
ON order_item(product_id);