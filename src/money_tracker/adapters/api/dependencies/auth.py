from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from money_tracker.infrastructure.postgres import get_db
from money_tracker.adapters.db.repositories.user_repo import PostgresUserRepository
from money_tracker.adapters.db.repositories.refresh_token_repo import PostgresRefreshTokenRepository
from money_tracker.application.use_cases.auth.register_user import RegisterUserUseCase
from money_tracker.application.use_cases.auth.login_google import LoginGoogleUseCase
from money_tracker.infrastructure.security.google import GoogleIdentityProvider
from money_tracker.infrastructure.security.jwt import JWTTokenProvider

async def get_register_use_case(db: AsyncSession = Depends(get_db)) -> RegisterUserUseCase:
    """Dependency Injection for RegisterUserUseCase"""
    user_repo = PostgresUserRepository(db)
    return RegisterUserUseCase(user_repo)

async def get_login_google_use_case(db: AsyncSession = Depends(get_db)) -> LoginGoogleUseCase:
    """Dependency Injection for LoginGoogleUseCase"""
    user_repo = PostgresUserRepository(db)
    refresh_token_repo = PostgresRefreshTokenRepository(db)
    identity_provider = GoogleIdentityProvider()
    token_provider = JWTTokenProvider()
    return LoginGoogleUseCase(identity_provider, token_provider, user_repo, refresh_token_repo)
