from fastapi import FastAPI
from app.core.config import settings
from app.api.endpoints import (
    agent, items, social, health, finance, alerts, real_estate, 
    categories, dependencies, settings as settings_endpoint
)

from contextlib import asynccontextmanager
from app.core.database import engine, Base, AsyncSessionLocal
# Import models to ensure they are registered with Base.metadata
from app import models 

# APScheduler for CRON jobs
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.services.finance_service import FinanceService

scheduler = AsyncIOScheduler()

async def process_recurring_job():
    """CRON job to process recurring transactions daily."""
    async with AsyncSessionLocal() as session:
        service = FinanceService(session)
        result = await service.process_recurring_transactions()
        print(f"[CRON] Recurring transactions processed: {result}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Start scheduler for recurring transactions
    scheduler.add_job(process_recurring_job, 'cron', hour=0, minute=1, id='recurring_sync')
    scheduler.start()
    print("[STARTUP] APScheduler started - recurring sync scheduled daily at 00:01")
    
    yield
    
    # Shutdown
    scheduler.shutdown()
    print("[SHUTDOWN] APScheduler stopped")

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

from fastapi.middleware.cors import CORSMiddleware

# Configure CORS - in production, replace with specific origins
origins = [
    "http://localhost:5173",  # Vite default
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://localhost:8000",
]

# Allow all origins in DEBUG mode
if settings.DEBUG:
    origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True if not settings.DEBUG else False,  # Can't use credentials with "*"
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
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


@app.get("/")
async def root():
    return {"message": "Welcome to LifeMap Agent API"}
