#!/bin/bash

docker stop solfedjio
docker rm solfedjio
docker image rm solfedjio
cd ..
docker build . --tag solfedjio
if [ "$( docker container inspect -f '{{.State.Running}}' postgres )" = "false" ]; then
  docker start postgres
  echo "Running database..."
  sleep 2
fi
docker run -p 8000:8000 -d --name solfedjio -e DB_URL=postgresql://postgres:postgres@172.28.1.1:5432/solfedjio_db solfedjio
docker network connect --ip 172.28.1.2 solfedjio-network solfedjio
docker network inspect solfedjio-network
