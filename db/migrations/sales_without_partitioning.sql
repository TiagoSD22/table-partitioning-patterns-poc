-- Create the main table
CREATE TABLE sales_without_partitioning (
    sale_id INT,
    sale_date DATE,
    amount DECIMAL(10, 2)
);

CREATE INDEX idx_sales_without_partitioning_date ON sales_without_partitioning (sale_date);