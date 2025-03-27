# Use a smaller base image
FROM python:3.6.9-slim-buster

# Set the working directory
WORKDIR /app

# Install necessary system packages and clean up
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    default-libmysqlclient-dev \
    libmariadb-dev-compat \
    libmariadb-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirement.txt /app/
RUN pip install --no-cache-dir -r requirement.txt

# Copy the application code
COPY . /app/

# Expose the application port
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

