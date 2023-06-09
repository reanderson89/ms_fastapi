#!/usr/bin/env bash
#
# These are all the "known good" Postman tests, run against a running Docker container:
#
# docker exec -it milestones_api /app/tests/postman.sh
#

# set -e

function show_error {
cat <<EOF

    _____      ____        ________     ____        _________     ____      _____   _____                                                                                                                            
   / ___ \    / __ \      (___  ___)   / __ \      (_   _____)   (    )    (_   _) (_   _)                                                                                                                           
  / /   \_)  / /  \ \         ) )     / /  \ \       ) (___      / /\ \      | |     | |                                                                                                                             
 ( (  ____  ( ()  () )       ( (     ( ()  () )     (   ___)    ( (__) )     | |     | |                                                                                                                             
 ( ( (__  ) ( ()  () )        ) )    ( ()  () )      ) (         )    (      | |     | |   __                                                                                                                        
  \ \__/ /   \ \__/ /        ( (      \ \__/ /      (   )       /  /\  \    _| |__ __| |___) )                                                                                                                       
   \____/     \____/         /__\      \____/        \_/       /__(  )__\  /_____( \________/                                                                                                                        
                                                                                                                                                                                                                     
 ______       ____           __      _     ____     ________        ____     ____     _____       _____        _____     ____   ________      __    __   ________   ________   _____      ______     ____     ____   
(_  __ \     / __ \         /  \    / )   / __ \   (___  ___)      / ___)   / __ \   (_   _)     (_   _)      / ___/    / ___) (___  ___)    (  \  /  ) (___  ___) (___  ___) (  __ \    (____  \   / __ \   / __ \  
  ) ) \ \   / /  \ \       / /\ \  / /   / /  \ \      ) )        / /      / /  \ \    | |         | |       ( (__     / /         ) )        \ (__) /      ) )        ) )     ) )_) )        ) /  ( (  ) ) ( (  ) ) 
 ( (   ) ) ( ()  () )      ) ) ) ) ) )  ( ()  () )    ( (        ( (      ( ()  () )   | |         | |        ) __)   ( (         ( (          ) __ (      ( (        ( (     (  ___/    __  / /   ( (  ) ) ( (  ) ) 
  ) )  ) ) ( ()  () )     ( ( ( ( ( (   ( ()  () )     ) )       ( (      ( ()  () )   | |   __    | |   __  ( (      ( (          ) )        ( (  ) )      ) )        ) )     ) )      /  \/ / __ ( (  ) ) ( (  ) ) 
 / /__/ /   \ \__/ /      / /  \ \/ /    \ \__/ /     ( (         \ \___   \ \__/ /  __| |___) ) __| |___) )  \ \___   \ \___     ( (          ) )( (      ( (        ( (     ( (      ( () \__/ / ( (__) ) ( (__) ) 
(______/     \____/      (_/    \__/      \____/      /__\         \____)   \____/   \________/  \________/    \____\   \____)    /__\        /_/  \_\     /__\       /__\    /__\      \__\____(   \____/   \____/  
                                                                                                                                                                                                                     

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
   "$SOURCE_DIR"/Milestones_message_templates.postman_collection.json
   "$SOURCE_DIR"/Milestones_messages.postman_collection.json
   "$SOURCE_DIR"/Milestones_programs.postman_collection.json
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
