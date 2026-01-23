#!/bin/bash

set -e  # Exit on error

echo "============================================"
echo "Starting Build Process..."
echo "============================================"

echo ""
echo "Step 1: Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Step 2: Running database migrations..."
python manage.py migrate --noinput

echo ""
echo "Step 3: Collecting static files..."
python manage.py collectstatic --noinput --clear

echo ""
echo "Step 4: Checking deployment configuration..."
python manage.py check --deploy --fail-level=WARNING || true

echo ""
echo "============================================"
echo "Build completed successfully!"
echo "============================================"
