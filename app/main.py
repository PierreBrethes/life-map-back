from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.endpoints import (
    agent, items, social, health, finance, alerts, real_estate, 
    categories, dependencies, settings as settings_endpoint
)

from contextlib import asynccontextmanager
from app.core.database import engine, Base
# Import models to ensure they are registered with Base.metadata
from app import models 

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown (if needed)

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

from fastapi.middleware.cors import CORSMiddleware

# Configure CORS
origins = [
    "http://localhost:5173",  # Vite default
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://localhost:8000",
    "*" # Allow all for development convenience
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(agent.router, prefix="/api/v1/agent", tags=["agent"])
app.include_router(items.router, prefix="/api/v1/items", tags=["items"])
app.include_router(categories.router, prefix="/api/v1/categories", tags=["categories"])
app.include_router(dependencies.router, prefix="/api/v1/dependencies", tags=["dependencies"])
app.include_router(social.router, prefix="/api/v1/social", tags=["social"])
app.include_router(health.router, prefix="/api/v1/health", tags=["health"])
app.include_router(finance.router, prefix="/api/v1/finance", tags=["finance"])
app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["alerts"])
app.include_router(real_estate.router, prefix="/api/v1/real-estate", tags=["real-estate"])
app.include_router(settings_endpoint.router, prefix="/api/v1/settings", tags=["settings"])


@app.get("/")
async def root():
    return {"message": "Welcome to LifeMap Agent API"}
