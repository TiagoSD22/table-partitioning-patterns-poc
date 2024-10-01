CREATE TABLE customers_without_partitioning (
    customer_id INT,
    customer_name VARCHAR(100),
    region VARCHAR(50)
);

CREATE INDEX idx_customer_without_partitioning_region ON customers_without_partitioning (region);