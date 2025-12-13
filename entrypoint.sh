#!/bin/bash
set -e

echo "🔄 Running database migrations..."

# Run Alembic migrations
python -m alembic upgrade head

echo "✅ Migrations complete!"

echo "🚀 Starting API server..."

# Execute the main command (uvicorn)
exec "$@"
