#!/bin/bash

cd db
docker build . --tag postgres
cd ../..
docker build . --tag solfedjio
docker run -p 5432:5432 -d --name postgres -e POSTGRES_PASSWORD=postgres postgres
echo "Creating database..."
sleep 4
docker exec --user postgres postgres psql -c "create database solfedjio_db"
docker network rm solfedjio-network
docker network create --subnet=172.28.0.0/16 solfedjio-network
docker network connect --ip 172.28.1.1 solfedjio-network postgres
docker run -p 8000:8000 -d --name solfedjio -e DB_URL=postgresql+asyncpg://postgres:postgres@172.28.1.1:5432/solfedjio_db solfedjio
docker network connect --ip 172.28.1.2 solfedjio-network solfedjio
docker network inspect solfedjio-network
