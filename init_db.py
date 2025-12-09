import asyncio
import sys
import os

# Add src to python path to emulate 'PYTHONPATH=src'
sys.path.append(os.path.join(os.getcwd(), "src"))

from money_tracker.infrastructure.postgres import engine, Base
# Import all models to ensure they are registered with Base metadata
from money_tracker.adapters.db.models.user import UserModel
from money_tracker.adapters.db.models.refresh_tokens import RefreshTokenModel
from money_tracker.core.config import get_settings

async def init_models():
    settings = get_settings()
    print(f"Connecting to {settings.DATABASE_URL}...")
    
    async with engine.begin() as conn:
        print("🗑️  Dropping all tables...")
        # Force drop specific tables that might cause dependency issues (e.g. legacy tables)
        from sqlalchemy import text
        await conn.execute(text("DROP TABLE IF EXISTS refresh_tokens CASCADE"))
        await conn.execute(text("DROP TABLE IF EXISTS users CASCADE"))
        
        await conn.run_sync(Base.metadata.drop_all)
        
        print("🏗️  Creating all tables...")
        await conn.run_sync(Base.metadata.create_all)
        
    print("✅ Database initialized successfully!")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_models())
