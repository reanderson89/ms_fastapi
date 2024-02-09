#!/usr/bin/env bash
#
# Initialization hooks:
# - https://docs.localstack.cloud/references/init-hooks/
#

apt install jq --assume-yes

QUEUES=(
  "localstack-accounts"
  "localstack-segment-query"
  "localstack-segment-response"
)

for Q_NAME in "${QUEUES[@]}"
do
  DLQ_NAME="${Q_NAME}-dlq"
  echo "Creating SQS queue named ${Q_NAME}"
  # -r to strip double quotes, capture the URL
  Q_URL=$(awslocal sqs create-queue --queue-name ${Q_NAME} | jq -r '.QueueUrl')

  echo "Creating DLQ queue named ${DLQ_NAME}"
  awslocal sqs create-queue --queue-name ${DLQ_NAME}

  echo "Configuring the DLQ for ${Q_NAME}"
  awslocal sqs set-queue-attributes \
    --queue-url ${Q_URL} \
    --attributes '{"RedrivePolicy": "{\"deadLetterTargetArn\":\"arn:aws:sqs:us-east-1:000000000000:'$DLQ_NAME'\",\"maxReceiveCount\":\"3\"}"}'
done
