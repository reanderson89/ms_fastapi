#!/usr/bin/env bash

# delete 'mariadb-data' folder from root directory
echo "Deleting 'mariadb-data' folder from root directory..."
rm -rf mariadb-data

# bring down and delete containers
echo "Bringing down and deleting containers..."
docker-compose down

# remove unused/dangling images
echo "Removing unused/dangling images..."
docker image prune -a

# run run.sh
echo "Running run.sh..."
./run.sh