#!/usr/bin/env bash
#
# Thhis script takes a Docker YAML file and sets the tag after "milestones-api"
#
# e.g. version.sh docker-file.yaml 1.2.3
#
# ...
# image:  blueboardinc/milestones-api:1.2.3
# ...
#

YAML_FILE=$1
VERSION=${2:-latest}


if [[ -z ${YAML_FILE} || -z ${VERSION} ]]; then
    printf "Missing required arguments, must pass YAML file and version"
    exit 1
fi

if [ ! -f ${YAML_FILE} ]; then
    printf "The YAML file ${YAML_FILE} does not exist..."
    exit 1
fi

# simply update the tag after milestones-api
sed -E "s/milestones-api:.*/milestones-api:${VERSION}/g" ${YAML_FILE}