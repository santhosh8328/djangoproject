FROM python:3.6.9-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && \
    apt-get install -y \
    gcc \
    libmariadb-dev-compat \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

# Copy and install Python dependencies
COPY requirement.txt /app/
RUN pip install --no-cache-dir -r requirement.txt

# Copy the application code
COPY . /app/

# Expose the port
EXPOSE 8000

# Use gunicorn as the entry point for production
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "testproject.wsgi:application"]
