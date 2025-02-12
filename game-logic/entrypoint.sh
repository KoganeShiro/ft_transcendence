#!/bin/sh

# sleep 10

# echo Run database migrations
# python manage.py migrate

redis-server --daemonize yes



# Start the server
exec "$@"




