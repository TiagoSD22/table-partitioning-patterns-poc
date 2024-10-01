CREATE TABLE customers (
    customer_id INT,
    customer_name VARCHAR(100),
    region VARCHAR(50)
)
PARTITION BY LIST (region);

CREATE INDEX idx_customer_region ON customers (region);

CREATE TABLE customers_p_north PARTITION OF customers
    FOR VALUES IN ('North', 'North-East', 'North-West');

CREATE TABLE customers_p_south PARTITION OF customers
    FOR VALUES IN ('South', 'South-East', 'South-West');

CREATE TABLE customers_p_central PARTITION OF customers
    FOR VALUES IN ('Central');