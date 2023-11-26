#!/bin/bash


# Check if the database exists
if psql  -U $POSTGRES_USER -lqt | cut -d \| -f 1 | grep -qw $POSTGRES_DB; then
  echo "Database '$POSTGRES_DB' already exists. Skipping creation."
else
  # Create the database
  psql  -U $POSTGRES_USER -c "CREATE DATABASE $POSTGRES_DB;"
  echo "Database '$POSTGRES_DB' created."
fi
