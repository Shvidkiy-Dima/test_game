#!/bin/bash

poetry run python /app/check_conn.py --service-name db --port 5432  --ip db
poetry run python /app/check_conn.py --service-name rabbit --port 5672  --ip rabbit


poetry run alembic upgrade head

cd app


poetry run python init_db.py

poetry run uvicorn main:app --reload --host $HOST --port $PORT