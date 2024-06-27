#!/bin/bash

URL=${1:-http://localhost:8080/alerts}
EXPECTED_STATUS_CODE=${2:-200}
RETRIES=${3:-3}
SLEEP_TIME=${4:-5}

for ((i=1; i<=RETRIES; i++)); do
  response=$(curl --write-out '%{http_code}' --silent --output /dev/null "$URL")
  if [ "$response" -eq "$EXPECTED_STATUS_CODE" ]; then
    echo "Health check passed"
    exit 0
  else
    echo "Attempt $i/$RETRIES failed: Expected status $EXPECTED_STATUS_CODE but got $response"
    sleep $SLEEP_TIME
  fi
done

echo "Health check failed after $RETRIES attempts"
exit 1
