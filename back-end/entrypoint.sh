#!/bin/sh

sleep 10

# Run database migrations
python manage.py migrate

# Start the server
exec "$@"