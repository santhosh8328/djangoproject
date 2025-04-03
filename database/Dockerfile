FROM mysql:8.0

# Set root password only (we’ll handle depl in the script)
ENV MYSQL_ROOT_PASSWORD=mysecretpassword \
    MYSQL_DATABASE=test_database

COPY init.sql /docker-entrypoint-initdb.d/01-init.sql
