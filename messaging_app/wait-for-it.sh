#!/bin/bash
# wait-for-it.sh

set -e

host="$1"
shift
port="$1"
shift
cmd="$@"

until nc -z "$host" "$port"; do
  echo "Waiting for '$host:$port' to be ready..."
  sleep 1
done

# Give an extra second for MySQL to really settle,
# especially after initial user/db creation.
echo "Host '$host:$port' is available. Waiting a bit more for MySQL readiness..."
sleep 5

echo "Executing command: $cmd"
exec $cmd