#!/bin/sh

echo 'Waiting for the DB to start...'
until nc -z "$MYSQL_HOST" "$MYSQL_PORT"; do
  sleep 1
done

echo "Collecting Static..."
python manage.py collectstatic --noinput

echo "Migrating the DB..."
python manage.py migrate

echo "Set Up Done! Proceeding further..."
exec "$@"