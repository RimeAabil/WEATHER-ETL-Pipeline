#!/usr/bin/env bash
set -e

# Create an admin user
superset fab create-admin \
              --username admin \
              --firstname Superset \
              --lastname Admin \
              --email admin@superset.com \
              --password admin

# Upgrade the database
superset db upgrade

# Setup roles
superset init

# Load examples (optional, controlled by env var)
if [ "$SUPERSET_LOAD_EXAMPLES" = "yes" ]; then
    superset load_examples
fi