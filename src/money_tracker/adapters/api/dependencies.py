from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from money_tracker.infrastructure.postgres import get_db
from money_tracker.adapters.db.repositories.user_repo import PostgresUserRepository
from money_tracker.application.use_cases.register_user import RegisterUserUseCase

async def get_register_use_case(db: AsyncSession = Depends(get_db)) -> RegisterUserUseCase:
    """Dependency Injection for RegisterUserUseCase"""
    user_repo = PostgresUserRepository(db)
    return RegisterUserUseCase(user_repo)
