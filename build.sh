#!/usr/bin/env bash

TAG=$1
DELETE=$2

# show tags:
# git tag -l | sort -V

if [ -z ${TAG} ]; then
    echo "Missing TAG, usage $0 v0.2.0 [delete]"
    exit 1
fi

# append the v
TAG=v${TAG}
# append the current gitsha
SHA=$(git rev-parse --short HEAD)
TAG=${TAG}-${SHA}

if [ -z ${DELETE} ]; then
    read -p "Tag and push as ${TAG}?  Are you sure? " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git tag ${TAG}
        git push origin ${TAG}
    fi    
    echo "Release tag:  $TAG"
else
    read -p "Delete tag ${TAG}?  Are you sure? " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git tag -d ${TAG}
        git push --delete origin ${TAG}
    fi
fi