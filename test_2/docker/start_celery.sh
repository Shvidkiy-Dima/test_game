#!/bin/bash

poetry run python /app/check_conn.py --service-name db --port 5432  --ip db
poetry run python /app/check_conn.py --service-name rabbit --port 5672  --ip rabbit


cd app

poetry run celery -A background_tasks worker --loglevel=DEBUG