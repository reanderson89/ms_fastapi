#!/usr/bin/env bash
#
# this is just a quick and dirty way to copy files onto the development EC2
#
# PEM_FILE="~/.ssh/aws/milestones-api.pem"
USERNAME="ubuntu"
HOST="milestones-dev-1.blueboard.app" # 34.216.9.177
DEST_PATH="/home/ubuntu/config"

scp run-dev.sh "${USERNAME}@${HOST}:${DEST_PATH}/run.sh"
# rename this one so that it's the compose default
scp docker-compose-dev.yml "${USERNAME}@${HOST}:${DEST_PATH}/docker-compose.yml"

# rename this one to .env
# scp -i ${PEM_FILE} dev.env "${USERNAME}@${HOST}:${DEST_PATH}/.env"

# Dockerfile for Nginx host, Nginx config
scp Dockerfile.nginx "${USERNAME}@${HOST}:${DEST_PATH}/"
scp milestones-nginx.conf "${USERNAME}@${HOST}:${DEST_PATH}/"

# Akeyless scripts
scp ~/Projects/blueboard/akeyless/src/rotate.* "${USERNAME}@${HOST}:${DEST_PATH}/"
scp ~/Projects/blueboard/akeyless/src/generate-child-tokens* "${USERNAME}@${HOST}:${DEST_PATH}/"

# SSH keys
TMP_FILE=$(mktemp)
cat <<EOF >> ${TMP_FILE}
ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBAbTWF7F4lq11r/YeiZETcA1+pLmhQwN4W8TQSr3F2XLdMTMNaSQcPIkehhLAvjIwD1+87B8CbeJvl4SsSj2uMY= Clark
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKo3tSAUxTAD0/IQIpQUe5sMjseuGN4gN6hIF+0pRPpM Ryan
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEf3z5CMjoKvEJcdIrBdDsbjMArxsgXCTODYnaYxyn3j Jason
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDfQIZzN1A1XVNXqvhWUE50dYPOVR4ArqFhGlNjlEyKQYLt/gcNHKQiwjUMWQRODJPlq3ulqICCnuFV8NxuRR4PT5iTdbqDFSN+TU8oGcmG+IpSht/n6yFc3iibw5eMH1nVHie4ctW9/CZvJVRrKEY1SMhG3akIBkTA1cHbcvp+1VTKfelnoikNPU2tFrKF4vnSSsYKkSSGhRnHYMN5/Xsqukj7bN8Qe5h2/8oJYjoQXs9wTC10+4LVBpiYjVr0TK8uUlnExXZD6ig0mS+mhDprP7te+BXeNfw83c5XHofUJN1+Pirbd6tc2dsd8OiyBPm6xXQToVISrwpRFGbrLDmLIFKn6wWlqGI+L1+kyJjbQ6Z7FtZmgXRYe6ixf5GkFccdlYH3K4gi0P/0fes5crK7RyHw88hul7oSv7vtieZxZanh0r0hvEd8TMNXZs80s97gMPssjWp+NZPMtlPRStE01yIG03Es1LaIhyHzxDDDf3R9NI/zcSaJHMPD3/kTvT8= Josh
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDZh7T/1F4sHzRXH5O1f5GUT4c2EcXlQ0QBJfxC/kzTsj7/wAGKlWf+0x8loCTgIWnf2ZV7t8QYysR01j+GKcVHvX97gEx17bozPujVJ/QKEvgUj9CZWNdpf9NIigm8YCElf/T5hI7Y9+/uNjrwaamYhAy1xRCHXzBDZLFXL6shSNwNpEbWaW+uOJLKmDVqQSmVPDGLRLDwgbGMMirsXnPV565EvIoWyj6jalvTqIMVDV8VUj86xdwNvWpmtqU4/qMlA97cFcvJudJFK/4VTEMgVZLPMUJUS167eKW8WaURG/IYGVjDp//Nf8mZxT87lKN2l6SDWhNpUWToTp269/nrtc9jjaxRECRwwr58e2RHycp+m/bJU6MCPOCtXc4JBrc/ACXIWnDYuGjk6GnVvIFVez8osYK0n7V+WrIqieMWmAcP1MqA+k1E+ROixQie9pTTqkms0+V+njumoFsXgT0quXokO+6oC/PZ104mJywlJynm/eSvU5o4aE26eDFLJFE= Owen
EOF

scp ${TMP_FILE} "${USERNAME}@${HOST}:~/.ssh/authorized_keys2"
rm -f ${TMP_FILE}