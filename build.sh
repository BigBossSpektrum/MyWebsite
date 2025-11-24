#!/usr/bin/env bash
set -o errexit

echo "Starting build process..."
echo ""

pip install -r requirements.txt

echo ""
echo "Running database diagnostics..."
python manage.py diagnose_db || true

echo ""
echo "Collecting static files..."
python manage.py collectstatic --no-input

echo ""
echo "Running migrations..."
python manage.py migrate

echo ""
echo "Setting up Site object..."
# Setup Site object for django.contrib.sites
python manage.py setup_site

echo ""
echo "Build completed successfully!"