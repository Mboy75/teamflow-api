#!/bin/sh

#!/bin/sh

echo "Waiting for database..."
sleep 5

echo "Running migrations..."
alembic upgrade head

echo "Seeding database..."
python -c "from app.db.base import SessionLocal; from app.db.seed import seed_data; db = SessionLocal(); seed_data(db); db.close()"

echo "Starting app..."

if [ "$ENV" = "dev" ]; then
  exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
else
  exec uvicorn app.main:app --host 0.0.0.0 --port 8000
fi