#!/usr/bin/env bash
#
# These are all the "known good" Postman tests, run against a running Docker container:
#
# docker exec -it milestones_api /app/tests/postman.sh
#

# set -e

function show_error {
   cat <<'EOF'

   ______         __           ______      _ __                                                               
  / ____/___     / /_____     / ____/___ _(_) /                                                               
 / / __/ __ \   / __/ __ \   / /_  / __ `/ / /                                                                
/ /_/ / /_/ /  / /_/ /_/ /  / __/ / /_/ / / /                                                                 
\____/\____/   \__/\____/  /_/ __ \__,_/_/_/     ____          __     __  __________________ ___   ____  ____ 
   / __ \____     ____  ____  / /_   _________  / / /__  _____/ /_   / / / /_  __/_  __/ __ \__ \ / __ \/ __ \
  / / / / __ \   / __ \/ __ \/ __/  / ___/ __ \/ / / _ \/ ___/ __/  / /_/ / / /   / / / /_/ /_/ // / / / / / /
 / /_/ / /_/ /  / / / / /_/ / /_   / /__/ /_/ / / /  __/ /__/ /_   / __  / / /   / / / ____/ __// /_/ / /_/ / 
/_____/\____/  /_/ /_/\____/\__/   \___/\____/_/_/\___/\___/\__/  /_/ /_/ /_/   /_/ /_/   /____/\____/\____/  
                                                                                                              
EOF
   return
}

SOURCE_DIR=/app/tests/postman
tests=(
   "$SOURCE_DIR"/Milestones_admins.postman_collection.json
   "$SOURCE_DIR"/Milestones_awards.postman_collection.json
   "$SOURCE_DIR"/Milestones_budgets.postman_collection.json
   "$SOURCE_DIR"/Milestones_clients.postman_collection.json
   "$SOURCE_DIR"/Milestones_client_awards.postman_collection.json
   "$SOURCE_DIR"/Milestones_events.postman_collection.json
   # "$SOURCE_DIR"/Milestones_message_templates.postman_collection.json
   # "$SOURCE_DIR"/Milestones_messages.postman_collection.json
   "$SOURCE_DIR"/Milestones_programs.postman_collection.json
   "$SOURCE_DIR"/Milestones_program_awards.postman_collection.json
   "$SOURCE_DIR"/Milestones_users.postman_collection.json
)

for test in "${tests[@]}"; do
   [ -f "$test" ] || break
   newman run $test
   status=$?
   if [ $status -ne 0 ]; then
      echo "There was a test failure in ${test}"
      # Knock yourself out:  https://patorjk.com/software/taag/#p=display&f=Doh&t=Test%20Failure
      show_error
      exit ${status}
   fi
done