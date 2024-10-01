import psycopg2
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

def generate_random_region():
    """Generate a random region."""
    regions = ['North', 'North-East', 'North-West', 'South', 'South-East', 'South-West', 'Central']
    return random.choice(regions)

def insert_random_customers_records(n):
    """Insert n random records into the customers table."""
    conn = get_db_connection()
    cursor = conn.cursor()

    customer_id = 1

    for _ in range(n):
        customer_name = f'Customer {customer_id}'
        region = generate_random_region()
        cursor.execute(
            "INSERT INTO customers (customer_id, customer_name, region) VALUES (%s, %s, %s)",
            (customer_id, customer_name, region)
        )
        cursor.execute(
            "INSERT INTO customers_without_partitioning (customer_id, customer_name, region) VALUES (%s, %s, %s)",
            (customer_id, customer_name, region)
        )
        customer_id += 1

    # Commit the transaction and close the connection
    conn.commit()
    cursor.close()
    conn.close()

def benchmark_query_execution():
    """Benchmark the execution time between the customers and customers_without_partitioning tables."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Define the query to benchmark
    query = "SELECT customer_id, customer_name, region FROM customers WHERE region = 'North';"

    # Benchmark the partitioned table
    cursor.execute(f"EXPLAIN ANALYZE {query}")
    partitioned_result = cursor.fetchall()
    partitioned_time = partitioned_result[-1][0]

    # Benchmark the non-partitioned table
    query_without_partitioning = query.replace("customers", "customers_without_partitioning")
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

print('Executing list_benchmark.py')
insert_random_customers_records(10000)
benchmark_query_execution()