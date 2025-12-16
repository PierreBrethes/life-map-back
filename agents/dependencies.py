"""
Dependencies for the LifeMap ADK Agent.

Provides async database session and service factories for direct service calls.
This avoids HTTP calls and enables direct database access from agent tools.
"""
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings

# === ASYNC DATABASE ENGINE (same config as app) ===
# Use pool settings optimized for agent usage
_engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

_SessionFactory = async_sessionmaker(
    bind=_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


@asynccontextmanager
async def get_async_session():
    """Get an async database session for agent tools."""
    async with _SessionFactory() as session:
        try:
            yield session
        finally:
            await session.close()


# === SERVICE FACTORIES ===
# These return service instances with a fresh session

async def get_category_service():
    """Get CategoryService with a database session."""
    from app.services.category_service import CategoryService
    async with _SessionFactory() as session:
        yield CategoryService(session)


async def get_item_service():
    """Get ItemService with a database session."""
    from app.services.item_service import ItemService
    async with _SessionFactory() as session:
        yield ItemService(session)


async def get_finance_service():
    """Get FinanceService with a database session."""
    from app.services.finance_service import FinanceService
    async with _SessionFactory() as session:
        yield FinanceService(session)


async def get_health_service():
    """Get HealthService with a database session."""
    from app.services.health_service import HealthService
    async with _SessionFactory() as session:
        yield HealthService(session)


async def get_social_service():
    """Get SocialService with a database session."""
    from app.services.social_service import SocialService
    async with _SessionFactory() as session:
        yield SocialService(session)


async def get_alert_service():
    """Get AlertService with a database session."""
    from app.services.alert_service import AlertService
    async with _SessionFactory() as session:
        yield AlertService(session)
