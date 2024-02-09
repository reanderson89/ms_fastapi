#!/bin/bash
trap 'docker-compose down' INT
docker-compose -f docker-compose-queue.yml logs -f
