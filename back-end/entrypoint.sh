#!/bin/sh

# sleep 10

echo Run database migrations
python manage.py migrate



# Create superuser if not exists
echo "from django.contrib.auth import get_user_model;
import os;
User = get_user_model();
username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'dfsdsdfsdfdsfds')
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'Superuser {username} created.')" | python manage.py shell


# Start the server
exec "$@"




