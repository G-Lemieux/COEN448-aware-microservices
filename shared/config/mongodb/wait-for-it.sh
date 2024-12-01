#!/usr/bin/env bash
#   Use this script to test if a given TCP host/port are available

set -e

TIMEOUT=300
QUIET=0
HOST="$1"
PORT="$2"

echo "Waiting for $HOST:$PORT..."

for i in $(seq $TIMEOUT) ; do
    nc -z "$HOST" "$PORT" && echo "MongoDB is up!" && exit 0
    sleep 1
done

echo "Operation timed out" >&2
exit 1