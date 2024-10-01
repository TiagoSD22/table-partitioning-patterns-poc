# About this project

This project demonstrates the use of table partitioning patterns in PostgreSQL to improve database performance. It includes scripts to insert and benchmark data in partitioned and non-partitioned tables, using different partitioning strategies such as range, list, and hash partitioning.

## Project Structure

```
.
├── db
│   ├── Dockerfile
│   └── migrations
│       ├── 01_create_tables.sql
│       └── 02_insert_data.sql
├── scripts
│   ├── Dockerfile
│   ├── hash_benchmark.py
│   ├── list_benchmark.py
│   └── range_benchmark.py
├── .env
└── docker-compose.yml
```

## Description

### Table Partitioning Patterns

Table partitioning is a database design technique used to improve performance and manageability. It involves dividing a large table into smaller, more manageable pieces called partitions. Each partition can be managed and accessed independently, which can lead to significant performance improvements for certain types of queries.

### Partitioning Strategies

- **Range Partitioning**: Divides the table into partitions based on a range of values in a specified column.
- **List Partitioning**: Divides the table into partitions based on a list of values in a specified column.
- **Hash Partitioning**: Divides the table into partitions based on a hash function applied to a specified column.

## Required Tools

- Docker
- Docker Compose
- Python 3.x

## Setup and Running the Project

### Step 1 Build and Run the Docker Containers

Use Docker Compose to build and run the containers:

```sh
docker-compose up --build
```

### Step 2: Run the Benchmark Scripts

The benchmark scripts will automatically run when the `tpp_poc_scripts` service starts. You can check the output in the Docker logs:

```sh
docker-compose logs -f tpp_poc_scripts
```

## Benchmark Scripts

### `hash_benchmark.py`

This script benchmarks the performance of inserting and querying data in a hash-partitioned table versus a non-partitioned table.

### `list_benchmark.py`

This script benchmarks the performance of inserting and querying data in a list-partitioned table versus a non-partitioned table.

### `range_benchmark.py`

This script benchmarks the performance of inserting and querying data in a range-partitioned table versus a non-partitioned table.

## Conclusion

Table partitioning can significantly improve the performance and manageability of large tables in a database. This project demonstrates how to implement and benchmark different partitioning strategies in PostgreSQL using Docker and Python.

Feel free to explore the scripts and modify them to suit your needs. Happy coding!