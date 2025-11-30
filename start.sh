#!/bin/bash
# Startup script for Render.com deployment
# Reads PORT from environment variable (set by Render) or defaults to 5000

PORT=${PORT:-5000}

echo "Starting application on port $PORT"

# Initialize database if needed
python -c "from models import init_db; init_db()" || echo "Database initialization skipped or failed"

# Start Gunicorn
exec gunicorn --bind "0.0.0.0:$PORT" --workers 2 --threads 2 --timeout 120 app:app

