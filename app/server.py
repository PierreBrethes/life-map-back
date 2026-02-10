"""
LifeMap Unified Server

Combines FastAPI (REST API) and Google ADK (AI Agent) in a single application.
Run with: python -m app.server
"""
import logging
from pathlib import Path

import uvicorn
from google.adk.cli.fast_api import get_fast_api_app

from app.core.config import settings
from app.api.endpoints import (
    agent, items, social, health, finance, alerts, real_estate,
    categories, dependencies, settings as settings_endpoint
)
from app.api.v1.endpoints import assets

from contextlib import asynccontextmanager
from app import models  # Register models with Base.metadata

# APScheduler for CRON jobs
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.finance_service import FinanceService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Configuration ===
HOST = "127.0.0.1"
PORT = 8000

scheduler = AsyncIOScheduler()


async def process_recurring_job():
    """CRON job to process recurring transactions daily."""
    async with AsyncSessionLocal() as session:
        service = FinanceService(session)
        result = await service.process_recurring_transactions()
        logger.info(f"[CRON] Recurring transactions processed: {result}")


# === Create ADK + FastAPI App ===
# google-adk 1.21.0 uses agents_dir (plural) - points to parent containing agents folder
AGENTS_DIR = str(Path(__file__).resolve().parent.parent)

app = get_fast_api_app(
    agents_dir=AGENTS_DIR,
    allow_origins=settings.cors_origins_list,
    web=True,  # Enable ADK Dev UI at /dev-ui
)

# === Lifespan Events ===
# Note: ADK's get_fast_api_app already has its own lifespan.
# We need to add our startup/shutdown logic differently.

@app.on_event("startup")
async def startup():
    """Startup: Create tables and start scheduler."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("[STARTUP] Database tables created/verified")
    
    scheduler.add_job(process_recurring_job, 'cron', hour=0, minute=1, id='recurring_sync')
    scheduler.start()
    logger.info("[STARTUP] APScheduler started - recurring sync scheduled daily at 00:01")


@app.on_event("shutdown")
async def shutdown():
    """Shutdown: Stop scheduler."""
    scheduler.shutdown()
    logger.info("[SHUTDOWN] APScheduler stopped")


# === Include LifeMap API Routers ===
app.include_router(agent.router, prefix="/api/agent", tags=["agent"])
app.include_router(items.router, prefix="/api/items", tags=["items"])
app.include_router(categories.router, prefix="/api/categories", tags=["categories"])
app.include_router(dependencies.router, prefix="/api/dependencies", tags=["dependencies"])
app.include_router(social.router, prefix="/api/social", tags=["social"])
app.include_router(health.router, prefix="/api/health", tags=["health"])
app.include_router(finance.router, prefix="/api/finance", tags=["finance"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["alerts"])
app.include_router(real_estate.router, prefix="/api/real-estate", tags=["real-estate"])
app.include_router(settings_endpoint.router, prefix="/api/settings", tags=["settings"])
app.include_router(assets.router, prefix="/api/assets", tags=["assets"])


@app.get("/", tags=["root"])
async def root():
    return {
        "message": "Welcome to LifeMap API",
        "docs": f"http://{HOST}:{PORT}/docs",
        "adk_ui": f"http://{HOST}:{PORT}/dev-ui",
    }


# === Run Server ===
if __name__ == "__main__":
    logger.info("🚀 Starting LifeMap Unified Server...")
    logger.info(f"📚 REST API Docs: http://{HOST}:{PORT}/docs")
    logger.info(f"🤖 ADK Agent UI: http://{HOST}:{PORT}/dev-ui")
    
    uvicorn.run(app, host=HOST, port=PORT, reload=False)
