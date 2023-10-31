#!/bin/sh


BACKEND_CONTAINER_NAME="backend"
ENV_FILE_PATH="./.env"
BACKEND_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $BACKEND_CONTAINER_NAME)

if [ -n "$BACKEND_IP" ]; then
    # Check if VITE_FKED already exists in the .env file
    if grep -q '^VITE_FKED=' "$ENV_FILE_PATH"; then
        # Update the existing VITE_FKED value
        sed -i "s/^VITE_FKED=.*/VITE_FKED=$BACKEND_IP/" "$ENV_FILE_PATH"
    else
        # Add VITE_FKED to the .env file
        echo "VITE_FKED=$BACKEND_IP" >> "$ENV_FILE_PATH"
    fi

    echo "Updated VITE_FKED in .env file."
else
    echo "Error: Unable to obtain the IP address of the backend container."
fi
