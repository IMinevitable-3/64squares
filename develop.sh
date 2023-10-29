#!/bin/bash
echo "Setting up environment..."

source env/bin/activate

if [[ $? -eq 0 ]]; then
  echo "Environment activated successfully."
  docker-compose build
  docker-compose up
else
  echo "Error: Failed to activate the environment."
fi
