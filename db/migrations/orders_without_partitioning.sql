CREATE TABLE orders_without_partitioning (
    order_id INT,
    order_date DATE,
    customer_id INT
);

CREATE INDEX idx_order_without_partitioning_customer_id ON orders_without_partitioning (customer_id);