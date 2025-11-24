#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

# Setup Site object for django.contrib.sites
python manage.py setup_site

echo "Build completed successfully!"