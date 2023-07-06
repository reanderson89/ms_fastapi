#!/usr/bin/env bash

#
# Check if the Docker network exists, and create if not
# see https://makeshiftinsights.com/blog/docker-swarm-communicate-between-stacks/
#

# NETWORK="blueboard-network"
# echo "Checking if the Docker network ${NETWORK} already exists"
# NETWORK_ID=$(docker network ls --filter name=${NETWORK} --quiet)
# if [ -z "${NETWORK_ID}" ]; then
#     echo "Creating a Docker network named ${NETWORK}"
#     docker network create --driver overlay --attachable ${NETWORK}
# else
#     echo "The Docker network ${NETWORK} already exists with an ID of ${NETWORK_ID}"
# fi

# docker stack deploy \
#     --compose-file docker-galera-swarm.yml \
#     galera

# echo "Next:"
# echo "docker service scale galera_seed=1"

# docker logs 
# docker service scale galera_node=3
