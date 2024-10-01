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

def insert_random_orders_records(n):
    """Insert n random records into the orders table."""
    # Database connection parameters
    conn = get_db_connection()
    cursor = conn.cursor()

    order_id = 1

    for _ in range(n):
        order_date = generate_random_date(datetime(2020, 1, 1), datetime(2022, 12, 31))
        customer_id = random.randint(1, 1000)
        cursor.execute(
            "INSERT INTO orders (order_id, order_date, customer_id) VALUES (%s, %s, %s)",
            (order_id, order_date, customer_id)
        )
        cursor.execute(
            "INSERT INTO orders_without_partitioning (order_id, order_date, customer_id) VALUES (%s, %s, %s)",
            (order_id, order_date, customer_id)
        )
        order_id += 1

    # Commit the transaction and close the connection
    conn.commit()
    cursor.close()
    conn.close()

def benchmark_query_execution():
    """Benchmark the execution time between the orders and orders_without_partitioning tables."""
    # Database connection parameters
    conn = get_db_connection()
    cursor = conn.cursor()

    # Define the query to benchmark
    query = "SELECT order_id, order_date, customer_id FROM orders WHERE customer_id = 500;"

    # Benchmark the partitioned table
    cursor.execute(f"EXPLAIN ANALYZE {query}")
    partitioned_result = cursor.fetchall()
    partitioned_time = partitioned_result[-1][0]

    # Benchmark the non-partitioned table
    query_without_partitioning = query.replace("orders", "orders_without_partitioning")
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

print('Executing hash_benchmark.py')
insert_random_orders_records(10000)
benchmark_query_execution()