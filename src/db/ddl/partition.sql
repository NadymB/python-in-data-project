-- Migrate "order" and "order_item" tables to use range partitioning by order_date.
-- Create partition table for order and order_item tables 
ALTER TABLE "order" RENAME TO order_old;
ALTER TABLE "order_item" RENAME TO order_item_old; 

CREATE TABLE "order" (
    order_id INT,
    order_date DATE,
    seller_id INT REFERENCES seller(seller_id),
    status VARCHAR(20) CHECK(status IN('PLACED', 'PAID', 'SHIPPED', 'DELIVERED', 'CANCELLED', 'RETURNED')),
    total_amount DECIMAL(12, 2) CHECK(total_amount >= 0),
    created_at DATE,
	PRIMARY KEY(order_id, order_date)
) PARTITION BY RANGE(order_date);

CREATE TABLE order_2025_08 PARTITION OF "order"
FOR VALUES FROM ('2025-08-01') TO ('2025-09-01');

CREATE TABLE order_2025_09 PARTITION OF "order"
FOR VALUES FROM ('2025-09-01') TO ('2025-10-01');

CREATE TABLE order_2025_10 PARTITION OF "order"
FOR VALUES FROM ('2025-10-01') TO ('2025-11-01');

INSERT INTO "order"
SELECT
    order_id,
    order_date,
    seller_id,
    status,
    total_amount,
    created_at
FROM order_old;

CREATE TABLE order_item (
    order_item_id INT,
    order_id INT,
    product_id INT REFERENCES product(product_id),
    order_date DATE,
    quantity INT CHECK(quantity > 0),
    unit_price DECIMAL(12, 2) CHECK(unit_price >= 0),
    subtotal DECIMAL(12, 2) CHECK(subtotal >= 0),
    created_at DATE,
	PRIMARY KEY (order_item_id, order_date),
	FOREIGN KEY (order_id, order_date) 
	REFERENCES "order"(order_id, order_date)
) PARTITION BY RANGE(order_date);

CREATE TABLE order_item_2025_08 PARTITION OF "order_item"
FOR VALUES FROM ('2025-08-01') TO ('2025-09-01');

CREATE TABLE order_item_2025_09 PARTITION OF "order_item"
FOR VALUES FROM ('2025-09-01') TO ('2025-10-01');

CREATE TABLE order_item_2025_10 PARTITION OF "order_item"
FOR VALUES FROM ('2025-10-01') TO ('2025-11-01');

INSERT INTO order_item
SELECT 
	order_item_id,
    order_id,
    product_id,
    order_date,
    quantity,
    unit_price,
    subtotal,
    created_at
FROM order_item_old;

DROP TABLE order_old, order_item_old;