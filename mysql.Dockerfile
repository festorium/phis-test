# Use MySQL base image
FROM mysql:latest

# Set environment variables
ENV MYSQL_ROOT_PASSWORD="adesiju1234"
ENV MYSQL_DATABASE="adminmanager"

# Expose MySQL port
EXPOSE 3306

# Define a command to run the database server
CMD ["mysqld"]