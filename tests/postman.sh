#!/usr/bin/env bash
#
# These are all the "known good" Postman tests, run against a running Docker container:
#
# docker exec -it milestones_api /app/tests/postman.sh
#

set -e

SOURCE_DIR=/app/tests/postman/
tests=(
   "$SOURCE_DIR"/Milestones_admins.postman_collection.json
   "$SOURCE_DIR"/Milestones_awards.postman_collection.json
   "$SOURCE_DIR"/Milestones_budgets.postman_collection.json
   "$SOURCE_DIR"/Milestones_clients.postman_collection.json
   "$SOURCE_DIR"/Milestones_client_awards.postman_collection.json
   "$SOURCE_DIR"/Milestones_events.postman_collection.json
   "$SOURCE_DIR"/Milestones_message_templates.postman_collection.json
   "$SOURCE_DIR"/Milestones_messages.postman_collection.json
   "$SOURCE_DIR"/Milestones_programs.postman_collection.json
   "$SOURCE_DIR"/Milestones_users.postman_collection.json
)

for test in "${tests[@]}"; do
    [ -f "$test" ] || break
   newman run $test
done