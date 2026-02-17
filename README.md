# LifeMap Backend

Backend API for **LifeMap** - a gamified 3D dashboard for managing your life.
Built with **FastAPI**, **PostgreSQL**, and **Google Gemini AI**.

## 🛠 Tech Stack

*   **Framework**: FastAPI (Python 3.11+)
*   **Database**: PostgreSQL 16
    *   **ORM**: SQLAlchemy 2.0 (Async)
    *   **Driver**: asyncpg
    *   **Extensions**: pgvector (for AI memory/RAG)
    *   **Migrations**: Alembic
*   **AI**: Google Generative AI (Gemini)
*   **Scheduling**: APScheduler (for recurring tasks & alerts)
*   **Package Manager**: Poetry

## 📦 Project Structure

The project follows a modular architecture:

```
life-map-back/
├── app/
│   ├── api/            # API Endpoints (Routes)
│   ├── core/           # Config, Database setup, Security
│   ├── models/         # SQLAlchemy Database Models (Finance, Health, etc.)
│   ├── schemas/        # Pydantic Schemas (Request/Response validation)
│   ├── services/       # Business Logic & External Integrations
│   └── main.py         # App Entrypoint
├── alembic/            # Database Migrations
├── tests/              # Test Suite
└── docker-compose.yml  # Container Orchestration
```

## ✨ Key Features (Modules)

*   **💰 Finance**: Transaction history, Subscriptions, Recurring flows, Asset valuation.
*   **🏠 Real Estate**: Property management, Maintenance tasks, Energy consumption.
*   **⚕️ Health**: Body metrics (weight, BMI), Medical appointments, Health records.
*   **👥 Social**: Contact management, Social calendar, Interaction frequency tracking.
*   **🤖 AI Agent**: Integrated Gemini assistant for natural language interaction and insights.
*   **🔔 Alerts System**: Automated monitoring for warnings and critical states (deadlines, maintenance).

## 🚀 Getting Started

### Prerequisites
*   Docker & Docker Compose
*   (Optional) Python 3.11+ and Poetry for local dev

### Environment Variables
Create a `.env` file at the root:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/lifemap
GOOGLE_API_KEY=your-gemini-api-key
DEBUG=true
```

### 🐳 Run with Docker (Recommended)

Start the API and Database containers:

```bash
docker-compose up --build
```
*   API: `http://localhost:8000`
*   Docs: `http://localhost:8000/docs`

### 💻 Local Development

Oprionnal : create and activate venv :
```bach
python3 -m venv .venv
source .venv/bin/activate
```

1.  **Install Dependencies**:
    ```bash
    pip install poetry
    poetry install
    ```

2.  **Run Server**:
    ```bash
    poetry run uvicorn app.server:app --reload
    ```

## 🗄 Database Migrations (Alembic)

Migrations run automatically on container startup. For manual management:

**Generate a migration** (after changing models):
```bash
docker exec lifemap-api python -m alembic revision --autogenerate -m "describe changes"
```

**Apply migrations**:
```bash
docker exec lifemap-api python -m alembic upgrade head
```

**View history**:
```bash
docker exec lifemap-api python -m alembic history
```

## 🤖 ADK Agent (IA Conversationnelle)

Le projet inclut un agent IA (Google ADK) qui peut interagir avec les données LifeMap en langage naturel.

### Structure de l'agent

```
agents/
├── agent.py              # Définition du root_agent
├── constants.py          # Configuration (model, nom, etc.)
├── prompts/
│   ├── system.md         # Instruction système
│   └── tools.md          # Description des outils
└── tools/
    ├── db_utils.py       # Helpers async → sync pour les services
    └── category_tools.py # Outils pour récupérer les îles
```

### Lancer l'agent en local

**Prérequis** :
*   Python 3.11+ avec `google-adk` installé
*   La base de données Postgres qui tourne (via Docker)
*   Le `.env` configuré avec `GOOGLE_API_KEY` et `DATABASE_URL` pointant vers `localhost`

**1. Installer les dépendances** (si pas déjà fait) :
```bash
pip install google-adk
```

**2. Lancer l'interface web ADK** :
```bash
cd life-map-back
python -m google.adk.cli web --port 8080
```

**3. Ouvrir l'interface** :
*   [http://localhost:8080](http://localhost:8080)
*   Sélectionner `agents` dans le menu déroulant
*   Poser une question : *"Quelles sont mes îles ?"*

> ⚠️ **Important** : Le `DATABASE_URL` dans `.env` doit pointer vers `localhost` (ex: `postgresql+asyncpg://postgres:postgres@localhost:5433/lifemap`) et non vers le nom du container Docker.
