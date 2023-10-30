#!/bin/bash
echo "Setting up environment..."

docker-compose  up -d postgres 
docker-compose  up -d redis
docker-compose up -d django-backend
docker-compose exec django-backend /bin/bash
