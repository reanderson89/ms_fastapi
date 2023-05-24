#!/usr/bin/env bash
#
# Run the Docker Swarm Stack
#
set -e

DH_USERNAME=${1:-}
DH_PASSWORD=${2:-} # password or personal access token
TAG=${3:-latest}

if [[ -z ${DH_USERNAME} || -z ${DH_PASSWORD} ]]; then
    printf "Missing required arguments, must pass Docker Hub username and personal access token\n"
    printf "Use single quotes to escape special chars\n"
    printf "Usage:\n"
    printf "$0 someusername 'dckr_pat_XXXXXXXXXXXXXXXXXXXXX'\n"
    exit 1
fi

echo ${DH_PASSWORD} | docker login --username ${DH_USERNAME} --password-stdin

docker stack deploy \
    --with-registry-auth \
    --compose-file docker-swarm.yml \
    milestones