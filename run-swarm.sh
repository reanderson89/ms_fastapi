#!/usr/bin/env bash
#
# Run the Docker Swarm Stack
#

set -e

# This can only be run on a node that's a manager, and so
# this will have an exit code of 1 if the node is a worker
MANAGER=$( docker node ls > /dev/null 2>&1 )
if [ $? -ne 0 ]; then
    echo "This swarm node is not a manager"
    exit 1
fi

DH_USERNAME=${1:-}
DH_PASSWORD=${2:-} # password or personal access token
SWARM_APP=${3:-milestones}

if [[ -z ${DH_USERNAME} || -z ${DH_PASSWORD} ]]; then
    printf "Missing required arguments, must pass Docker Hub username and personal access token\n"
    printf "Use single quotes to escape special chars\n"
    printf "Usage:\n"
    printf "$0 someusername 'dckr_pat_XXXXXXXXXXXXXXXXXXXXX'\n"
    exit 1
fi

echo ${DH_PASSWORD} | docker login --username ${DH_USERNAME} --password-stdin

echo "Deploying stack"

# Checking that the docker network exists is done in gelera startup, which should be done before
# this script is run
# see https://makeshiftinsights.com/blog/docker-swarm-communicate-between-stacks/

NETWORK="blueboard-network"
echo "Checking if the Docker network ${NETWORK} already exists"
NETWORK_ID=$(docker network ls --filter name=${NETWORK} --quiet)
if [ -z "${NETWORK_ID}" ]; then
    echo "Creating a Docker network named ${NETWORK}"
    docker network create --driver overlay --attachable ${NETWORK}
else
    echo "The Docker network ${NETWORK} already exists with an ID of ${NETWORK_ID}"
fi


case ${SWARM_APP} in
  milestones)
    docker stack deploy \
    --with-registry-auth \
    --compose-file docker-milestones-swarm.yml \
    milestones
    ;;

  api)
    docker stack deploy \
    --with-registry-auth \
    --compose-file docker-api-swarm.yml \
    api
    ;;

  *)
    echo "Unknown Docker Swarm app name \"${SWARM_APP}\""
    ;;
esac
