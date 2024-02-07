#!/usr/bin/env bash
# get the IP address of the localstack container and add it to the DNS resolver for this host

LOCALSTACK_IP=$(dig yass_localstack +short)
if [ ! -z "${LOCALSTACK_IP}"  ]; then
  echo "Adding $LOCALSTACK_IP to DNS resolver"
  cat <<EOF > /etc/resolv.conf
# This file was auto-generated to include the IP of the
# Localstack container in the list of DNS servers to query
search localdomain
nameserver $LOCALSTACK_IP
nameserver 127.0.0.11
options ndots:0
EOF
fi