#!/bin/sh

# sleep 10

echo Run database migrations
python manage.py migrate

# Create superuser admin if not exists
echo "from django.contrib.auth import get_user_model;
import os;
User = get_user_model();
username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'dfsdsdfsdfdsfds')
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'Superuser {username} created.')" | python manage.py shell


# # Create gamesuperiser if not exists
# echo "from django.contrib.auth import get_user_model;
# import os;
# User = get_user_model();
# username = os.getenv('GAMESERVICE_USERNAME', 'gameservice')
# email = os.getenv('GAMESERVICE_EMAIL', 'game@service.com')
# password = os.getenv('GAMESERVICE_PASSWORD', 'gameservicepwd')
# if not User.objects.filter(username=username).exists():
#     User.objects.create_superuser(username, email, password)
#     print(f'Gameserviceuser {username} created.')" | python manage.py shell

# Create api_user if not exists
echo "from django.contrib.auth import get_user_model;
import os;
User = get_user_model();
username = 'api_user'
email = 'api_user@api.fr'
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email)
    print(f'APIuser {username} created.')" | python manage.py shell


# Start the server
exec "$@"




