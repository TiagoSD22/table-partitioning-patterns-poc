# Use the latest Python image from the Docker Hub
FROM python:latest

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run all .py files in the /app directory
CMD for file in /app/*.py; do python "$file"; done