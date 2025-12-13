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

## Database Migrations (Alembic)

Les migrations sont exécutées **automatiquement** au démarrage du conteneur. Pour les cas où tu as besoin de gérer les migrations manuellement :

### Créer une nouvelle migration (auto-détectée depuis les modèles)

```bash
docker exec lifemap-api python -m alembic revision --autogenerate -m "description de la migration"
```

### Créer une migration manuelle (vide)

```bash
docker exec lifemap-api python -m alembic revision -m "description de la migration"
```

### Appliquer toutes les migrations

```bash
docker exec lifemap-api python -m alembic upgrade head
```

### Revenir à la migration précédente

```bash
docker exec lifemap-api python -m alembic downgrade -1
```

### Voir l'historique des migrations

```bash
docker exec lifemap-api python -m alembic history
```

### Voir la migration actuelle

```bash
docker exec lifemap-api python -m alembic current
```

## API Docs

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
