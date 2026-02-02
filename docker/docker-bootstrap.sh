#!/usr/bin/env bash
set -e

# Start Superset
if [ "$#" -eq 0 ] || [ "$1" = "app" ]; then
    gunicorn \
        --bind "0.0.0.0:${SUPERSET_PORT:-8088}" \
        --access-logfile '-' \
        --error-logfile '-' \
        --workers 1 \
        --worker-class gthread \
        --threads 20 \
        --timeout 60 \
        --limit-request-line 0 \
        --limit-request-field_size 0 \
        "superset.app:create_app()"
else
    exec "$@"
fi