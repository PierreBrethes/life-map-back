# LifeMap Backend

Backend API for LifeMap - a gamified 3D dashboard for managing your life.

## Requirements

- Python 3.11+
- PostgreSQL

## Environment Variables

Create a `.env` file at the root:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/lifemap
GOOGLE_API_KEY=your-gemini-api-key
DEBUG=true  # Optional: enables SQL logging and CORS wildcard
```

## Local Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn app.main:app --reload
```

## Docker

```bash
docker-compose up --build
```

API available at `http://localhost:8000`

## API Docs

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
