#!/bin/bash
trap 'docker-compose down' INT
docker-compose logs -f milestones_db milestones_api
