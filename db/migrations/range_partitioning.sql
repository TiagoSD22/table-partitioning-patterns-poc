-- Create the main table
CREATE TABLE sales (
    sale_id INT,
    sale_date DATE,
    amount DECIMAL(10, 2)
)
PARTITION BY RANGE (sale_date);

CREATE INDEX idx_sale_date ON sales (sale_date);

-- Create partitions
CREATE TABLE sales_p2019 PARTITION OF sales
    FOR VALUES FROM ('2019-01-01') TO ('2020-01-01');

CREATE TABLE sales_p2020 PARTITION OF sales
    FOR VALUES FROM ('2020-01-01') TO ('2021-01-01');

CREATE TABLE sales_p2021 PARTITION OF sales
    FOR VALUES FROM ('2021-01-01') TO ('2022-01-01');