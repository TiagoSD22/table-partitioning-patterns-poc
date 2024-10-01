import psycopg2
from datetime import datetime, timedelta
import random
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def get_db_connection():
    """Get a database connection using environment variables."""
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT")
    )

def generate_random_date(start_date, end_date):
    """Generate a random date between start_date and end_date."""
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

def insert_random_sales_records(n):
    """Insert n random records into the sales table."""
    # Database connection parameters
    conn = get_db_connection()
    cursor = conn.cursor()

    # Define date ranges for partitions
    date_ranges = [
        (datetime(2019, 1, 1), datetime(2019, 12, 31)),
        (datetime(2020, 1, 1), datetime(2020, 12, 31)),
        (datetime(2021, 1, 1), datetime(2021, 12, 31))
    ]

    # Calculate the number of records per partition
    records_per_partition = n // len(date_ranges)
    remaining_records = n % len(date_ranges)

    sale_id = 1

    for start_date, end_date in date_ranges:
        for _ in range(records_per_partition):
            sale_date = generate_random_date(start_date, end_date)
            amount = round(random.uniform(100.00, 5000.00), 2)
            cursor.execute(
                "INSERT INTO sales (sale_id, sale_date, amount) VALUES (%s, %s, %s)",
                (sale_id, sale_date, amount)
            )
            cursor.execute(
                "INSERT INTO sales_without_partitioning (sale_id, sale_date, amount) VALUES (%s, %s, %s)",
                (sale_id, sale_date, amount)
            )
            sale_id += 1

    # Distribute remaining records
    for _ in range(remaining_records):
        start_date, end_date = random.choice(date_ranges)
        sale_date = generate_random_date(start_date, end_date)
        amount = round(random.uniform(100.00, 5000.00), 2)
        cursor.execute(
            "INSERT INTO sales (sale_id, sale_date, amount) VALUES (%s, %s, %s)",
            (sale_id, sale_date, amount)
        )
        cursor.execute(
            "INSERT INTO sales_without_partitioning (sale_id, sale_date, amount) VALUES (%s, %s, %s)",
            (sale_id, sale_date, amount)
        )
        sale_id += 1

    # Commit the transaction and close the connection
    conn.commit()
    cursor.close()
    conn.close()

def benchmark_query_execution():
    """Benchmark the execution time between the sales and sales_without_partitioning tables."""
    # Database connection parameters
    conn = get_db_connection()
    cursor = conn.cursor()

    # Define the query to benchmark
    query = "SELECT sale_id, sale_date, amount FROM sales WHERE sale_date >= '2021-01-01' AND sale_date < '2022-01-01';"

    # Benchmark the partitioned table
    cursor.execute(f"EXPLAIN ANALYZE {query}")
    partitioned_result = cursor.fetchall()
    partitioned_time = partitioned_result[-1][0]

    # Benchmark the non-partitioned table
    query_without_partitioning = query.replace("sales", "sales_without_partitioning")
    cursor.execute(f"EXPLAIN ANALYZE {query_without_partitioning}")
    non_partitioned_result = cursor.fetchall()
    non_partitioned_time = non_partitioned_result[-1][0]

    # Print the results
    print("Partitioned Table Execution Time:")
    print(partitioned_time)
    print("\nNon-Partitioned Table Execution Time:")
    print(non_partitioned_time)

    # Calculate the percentage difference
    partitioned_time_value = float(partitioned_time.split(" ")[2])
    non_partitioned_time_value = float(non_partitioned_time.split(" ")[2])
    percentage_difference = ((non_partitioned_time_value - partitioned_time_value) / partitioned_time_value) * 100

    if partitioned_time_value < non_partitioned_time_value:
        print(f"Partitioned table was {abs(percentage_difference):.2f}% faster than non-partitioned table.")
    else:
        print(f"Non-partitioned table was {abs(percentage_difference):.2f}% faster than partitioned table.")

    # Close the connection
    cursor.close()
    conn.close()

print('Executing range_benchmark.py')
insert_random_sales_records(10000)
benchmark_query_execution()

