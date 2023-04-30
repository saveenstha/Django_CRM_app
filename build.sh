#!/bin/bash

#Build the project
echo "Building the project..."
python3.9 -m pip install -r requirements.txt

echo "Make Migrations... "
python3.9 manage.py makemigrations --noinput
python3.9 manage.py migrate --noinput

echo "Collect Static..."
python3.9 manage.py collectstatic --noinput --clear

#echo "Start server..."
#gunicorn djcrm.wsgi:application --bind=0.0.0.0:SPORT --workers=4
