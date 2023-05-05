#!/usr/bin/env bash

REPO="blueboardinc/milestones-api"
TAG="latest"

docker build -f Dockerfile.milestones_api -t ${REPO}:${TAG} .
docker push ${REPO}:${TAG}