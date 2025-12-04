from typing import Optional
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from money_tracker.domain.models.user import User
from money_tracker.application.ports.repositories.user_repo import UserRepository
from money_tracker.adapters.db.models import UserModel

class PostgresUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_entity(self, model: UserModel) -> User:
        """Convert SQLAlchemy Model to Domain Entity."""
        return User(
            id=model.id,
            email=model.email,
            password_hash=model.password_hash,
            full_name=model.full_name,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _to_model(self, entity: User) -> UserModel:
        """Convert Domain Entity to SQLAlchemy Model."""
        return UserModel(
            id=entity.id,
            email=entity.email,
            password_hash=entity.password_hash,
            full_name=entity.full_name,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    async def save(self, user: User) -> User:
        model = self._to_model(user)
        # Check if exists to decide merge (update) or add (insert)
        # For simplicity in this MVP, we'll use merge which handles both
        await self.session.merge(model)
        await self.session.commit()
        return user

    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        result = await self.session.execute(select(UserModel).where(UserModel.id == user_id))
        model = result.scalar_one_or_none()
        if model:
            return self._to_entity(model)
        return None

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(select(UserModel).where(UserModel.email == email))
        model = result.scalar_one_or_none()
        if model:
            return self._to_entity(model)
        return None
