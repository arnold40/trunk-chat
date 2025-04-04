#!/bin/bash

# Run migrations
python manage.py migrate --noinput

# Start the server
exec "$@"
