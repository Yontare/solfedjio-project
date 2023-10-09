echo "Running database..."
docker start postgres
sleep 1
echo "Running application..."
docker start solfedjio