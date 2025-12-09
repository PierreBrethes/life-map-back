import asyncio
import logging
from app.core.database import engine, Base
from app.models import * # Import all models to ensure they are registered with Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all) # Optional: reset db
        logger.info("Creating all tables...")
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Tables created successfully!")

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_db())
