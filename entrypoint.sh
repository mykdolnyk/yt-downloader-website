#!/bin/sh

echo "Collecting Static..."
python manage.py collectstatic

echo "Migrating the DB..."
python manage.py migrate

echo "Set Up Done! Proceeding further..."
exec "$@"