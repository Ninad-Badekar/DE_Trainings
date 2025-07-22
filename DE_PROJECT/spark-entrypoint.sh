#!/bin/bash

# Fix missing user issue (if running as UID 1001 without entry in /etc/passwd)
if ! id "$(whoami)" &>/dev/null; then
  echo "spark:x:$(id -u):$(id -g):Spark User:/home/spark:/bin/bash" >> /etc/passwd
fi

# Set Ivy cache directories to avoid null pointer issue
export SPARK_SUBMIT_OPTS="-Divy.cache.dir=/tmp/.ivy2 -Divy.home=/tmp/.ivy2"

# Create the Ivy directories if they don't exist
mkdir -p /tmp/.ivy2

# Execute the main container command
exec "$@"
