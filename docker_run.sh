#!/bin/bash

set -e  # Exit on any error

# Function to display messages
echoinfo() {
    printf "\e[36m%s\e[0m\n" "$@"
}

# Function to display error messages
echoerror() {
    printf "\e[31m%s\e[0m\n" "$@"
}

# Wait for the DB to be ready
echoinfo "Waiting for PostgreSQL to become available..."
counter=0
until nc -z db 5432
do
    sleep 1
    counter=$((counter + 1))
    if [ $counter -ge 60 ]; then  # Wait max of 60 seconds
        echoerror "PostgreSQL was not available within 60 seconds, exiting..."
        exit 1
    fi
done

echoinfo "PostgreSQL is up, continuing..."

# Create migration files
echoinfo "Creating migration files..."
python manage.py makemigrations || {
    echoerror "Failed to create migration files"
    exit 1
}

# Apply database migrations
echoinfo "Applying database migrations..."
python manage.py migrate --noinput || {
    echoerror "Failed to apply database migrations"
    exit 1
}


echoinfo "Checking for existing superuser..."
if echo "from django.contrib.auth.models import User; print(User.objects.filter(email='byurtkulu@outlook.com', is_superuser=True).exists())" | python manage.py shell | grep -q "False"; then
    echoinfo "Creating superuser..."
    echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'byurtkulu@outlook.com', 'password')" | python manage.py shell || {
        echoerror "Failed to create superuser"
        exit 1
    }
else
    echoinfo "Superuser with email 'byurtkulu@outlook.com' already exists, skipping..."
fi


# Start the server
echoinfo "Starting the server..."
exec python manage.py runserver 0.0.0.0:8000
