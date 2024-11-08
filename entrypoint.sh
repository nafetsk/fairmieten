#!/bin/sh
IP="${1:-0.0.0.0}"
PORT="${2:-8001}"

echo "Initializing my application"

poetry run python3 manage.py migrate
#poetry run python manage.py shell -c "from aggregation.test_data import create_test_data;"
#poetry run python manage.py shell -c "from fairmieten import insert_initial_data;"

echo "Starting my application on ${IP}:${PORT}..."
poetry run python3 manage.py runserver ${IP}:${PORT}
