import asyncio
from sqlalchemy import text
from app.core.database import engine
from app.models.asset_config import AssetConfig

async def reset_table():
    async with engine.begin() as conn:
        print("Dropping table asset_configs...")
        await conn.execute(text("DROP TABLE IF EXISTS asset_configs"))
        print("Table dropped.")
        
        print("Recreating tables...")
        # Since we can't easily isolate just one table creation with create_all without metadata manipulation,
        # and create_all is safe for existing tables, we run it for all.
        # But to be clean, let's just create this one if possible, or rely on create_all.
        from app.core.database import Base
        await conn.run_sync(Base.metadata.create_all)
        print("Tables created.")

if __name__ == "__main__":
    asyncio.run(reset_table())
