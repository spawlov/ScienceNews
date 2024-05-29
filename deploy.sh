#!/bin/bash
set -e
echo
echo "Starting deploy..."
echo "=================================================================="
echo "Pull from repository..."
git pull
echo "Pull from repository completed."
echo "=================================================================="
echo "Activating venv..."
source .science_news/bin/activate
echo "Venv activated."
echo "=================================================================="
echo "Updating requirements..."
pip install -r requirements.txt
echo "Requirements updated."
echo "=================================================================="
echo "Collecting staticfiles..."
python manage.py collectstatic --noinput
echo "Staticfiles collected."
echo "=================================================================="
echo "Migrations are applied..."
python manage.py migrate --noinput
echo "Migrations completed."
echo "=================================================================="
echo "Restarting Gunicorn..."
sudo systemctl restart sciencenews.service
echo "Restart Gunicorn completed."
echo "=================================================================="
echo "Restarting Celery..."
sudo systemctl restart sc-celery.service
echo "Restart Celery completed."
echo "=================================================================="
echo "Restarting Flower..."
sudo systemctl restart flower.service
echo "Restart Flower completed."
echo "=================================================================="
echo "Reloading Nginx..."
sudo systemctl reload nginx
echo "Nginx reloaded"
echo "=================================================================="
echo "Deactivating venv..."
deactivate
echo "=================================================================="
chmod a+x deploy.sh
echo "Deploy completed."
