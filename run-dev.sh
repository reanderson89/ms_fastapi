#!/usr/bin/env bash
#
# Note: Starting with Docker Compose v2, Docker has migrated towards using the
# compose CLI plugin command, and away from the original docker-compose
#
# This script assumes that has been installed
#

set -e

DH_USERNAME=${1:-}
DH_PASSWORD=${2:-} # password or personal access token
TAG=${3:-latest}
AK_TOKEN=${4:-"no-token"}

src_dir=$(dirname "$0") # curent working directory of this script
COMPOSE_FILE="${src_dir}/docker-compose.yml"

echo "Preparing to build using Docker tag ${TAG}..."

if [[ -z ${DH_USERNAME} || -z ${DH_PASSWORD} ]]; then
    printf "Missing required arguments, must pass Docker Hub username and password/token\n"
    printf "Use single quotes to escape special chars\n"
    printf "Usage:\n"
    printf "$0 someusername 'fo3$a5a'\n"
    exit 1
fi

if [ ! -f ${COMPOSE_FILE} ]; then
    printf "The compose file ${COMPOSE_FILE} does not exist..."
    exit 1
fi

echo "Writing tag \"${TAG}\" to .env file"
cat << EOF > /home/ubuntu/config/.env
TAG=${TAG}
EOF

echo ${DH_PASSWORD} | docker login --username ${DH_USERNAME} --password-stdin

echo "Building new containers..."
AKEYLESS_TOKEN=${AK_TOKEN} docker compose build

echo "Stopping and starting containers..."
docker compose down
AKEYLESS_TOKEN=${AK_TOKEN} docker compose --file ${COMPOSE_FILE} up --detach