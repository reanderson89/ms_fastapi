#!/usr/bin/env bash
#
# These are all the "known good" Postman tests, run against a running Docker container:
#
# docker exec -it milestones_api /app/tests/postman.sh
#

# set -e

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
      echo "\nThere was a test failure in ${test}"
      # Knock yourself out:  https://patorjk.com/software/taag/#p=display&f=Doh&t=Test%20Failure
      cat <<EOT
                                                                                                                                              
                                                                                                                                                                                                   
                                                                                                                                                                                                   
TTTTTTTTTTTTTTTTTTTTTTT                                          tttt               FFFFFFFFFFFFFFFFFFFFFF                  iiii  lllllll                                                          
T:::::::::::::::::::::T                                       ttt:::t               F::::::::::::::::::::F                 i::::i l:::::l                                                          
T:::::::::::::::::::::T                                       t:::::t               F::::::::::::::::::::F                  iiii  l:::::l                                                          
T:::::TT:::::::TT:::::T                                       t:::::t               FF::::::FFFFFFFFF::::F                        l:::::l                                                          
TTTTTT  T:::::T  TTTTTTeeeeeeeeeeee        ssssssssss   ttttttt:::::ttttttt           F:::::F       FFFFFFaaaaaaaaaaaaa   iiiiiii  l::::l uuuuuu    uuuuuu rrrrr   rrrrrrrrr       eeeeeeeeeeee    
        T:::::T      ee::::::::::::ee    ss::::::::::s  t:::::::::::::::::t           F:::::F             a::::::::::::a  i:::::i  l::::l u::::u    u::::u r::::rrr:::::::::r    ee::::::::::::ee  
        T:::::T     e::::::eeeee:::::eess:::::::::::::s t:::::::::::::::::t           F::::::FFFFFFFFFF   aaaaaaaaa:::::a  i::::i  l::::l u::::u    u::::u r:::::::::::::::::r  e::::::eeeee:::::ee
        T:::::T    e::::::e     e:::::es::::::ssss:::::stttttt:::::::tttttt           F:::::::::::::::F            a::::a  i::::i  l::::l u::::u    u::::u rr::::::rrrrr::::::re::::::e     e:::::e
        T:::::T    e:::::::eeeee::::::e s:::::s  ssssss       t:::::t                 F:::::::::::::::F     aaaaaaa:::::a  i::::i  l::::l u::::u    u::::u  r:::::r     r:::::re:::::::eeeee::::::e
        T:::::T    e:::::::::::::::::e    s::::::s            t:::::t                 F::::::FFFFFFFFFF   aa::::::::::::a  i::::i  l::::l u::::u    u::::u  r:::::r     rrrrrrre:::::::::::::::::e 
        T:::::T    e::::::eeeeeeeeeee        s::::::s         t:::::t                 F:::::F            a::::aaaa::::::a  i::::i  l::::l u::::u    u::::u  r:::::r            e::::::eeeeeeeeeee  
        T:::::T    e:::::::e           ssssss   s:::::s       t:::::t    tttttt       F:::::F           a::::a    a:::::a  i::::i  l::::l u:::::uuuu:::::u  r:::::r            e:::::::e           
      TT:::::::TT  e::::::::e          s:::::ssss::::::s      t::::::tttt:::::t     FF:::::::FF         a::::a    a:::::a i::::::il::::::lu:::::::::::::::uur:::::r            e::::::::e          
      T:::::::::T   e::::::::eeeeeeee  s::::::::::::::s       tt::::::::::::::t     F::::::::FF         a:::::aaaa::::::a i::::::il::::::l u:::::::::::::::ur:::::r             e::::::::eeeeeeee  
      T:::::::::T    ee:::::::::::::e   s:::::::::::ss          tt:::::::::::tt     F::::::::FF          a::::::::::aa:::ai::::::il::::::l  uu::::::::uu:::ur:::::r              ee:::::::::::::e  
      TTTTTTTTTTT      eeeeeeeeeeeeee    sssssssssss              ttttttttttt       FFFFFFFFFFF           aaaaaaaaaa  aaaaiiiiiiiillllllll    uuuuuuuu  uuuurrrrrrr                eeeeeeeeeeeeee  
                                                                                                                                                                                                                                                                                                                                          
EOT
      exit ${status}
   fi
done