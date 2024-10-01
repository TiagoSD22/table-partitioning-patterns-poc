# Use the latest PostgreSQL image from Docker Hub
FROM postgres:latest

# Copy migration files to the Docker container
COPY migrations /docker-entrypoint-initdb.d/

# Expose PostgreSQL port
EXPOSE 5432