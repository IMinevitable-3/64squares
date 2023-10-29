#!/bin/bash

# Wait for PostgreSQL to be ready
until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DB" > /dev/null 2>&1; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 1
done

# Check if the database exists
if ! psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT 1" > /dev/null 2>&1; then
  # Create the database
  echo "Creating database..."
  createdb -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -e "$POSTGRES_DB"
fi

echo "Database is ready!"

# Run the original command (CMD or ENTRYPOINT)
exec "$@"
