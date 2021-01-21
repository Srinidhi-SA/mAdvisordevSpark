#!/bin/sh
python manage.py makemigrations
echo "Makemigrations done!!!"
python manage.py migrate
echo "Migrate done!!!"
echo "Exiting..."

