import asyncio
import sys
import os

# Add src to python path
sys.path.append(os.path.join(os.getcwd(), "src"))

from money_tracker.infrastructure.postgres import engine, AsyncSessionLocal, Base
from money_tracker.domain.models.user import User
from money_tracker.adapters.db.repositories.user_repo import PostgresUserRepository
from money_tracker.adapters.db.models import UserModel # Import to register with Base

async def main():
    # 1. Create Tables (Quick & Dirty for verification)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all) # Reset DB
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tables created.")

    # 2. Use Repository
    async with AsyncSessionLocal() as session:
        repo = PostgresUserRepository(session)
        
        # Create User
        new_user = User(
            email="adapter_test@example.com",
            password_hash="secret123",
            full_name="Adapter Tester"
        )
        
        print(f"💾 Saving user: {new_user.email}...")
        saved_user = await repo.save(new_user)
        print("✅ User saved.")

        # Get User
        print(f"🔍 Fetching user by ID: {saved_user.id}...")
        fetched_user = await repo.get_by_id(saved_user.id)
        
        if fetched_user:
            print(f"✅ User found: {fetched_user.full_name} ({fetched_user.email})")
            assert fetched_user.id == saved_user.id
            assert fetched_user.email == "adapter_test@example.com"
        else:
            print("❌ User NOT found!")

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())
