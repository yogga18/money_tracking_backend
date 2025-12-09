from typing import Optional
import uuid
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from money_tracker.domain.models.refresh_token import RefreshToken
from money_tracker.application.ports.repositories.refresh_token_repo import RefreshTokenRepository
from money_tracker.adapters.db.models.refresh_tokens import RefreshTokenModel

class PostgresRefreshTokenRepository(RefreshTokenRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_entity(self, model: RefreshTokenModel) -> RefreshToken:
        """Convert SQLAlchemy Model to Domain Entity."""
        return RefreshToken(
            id=model.id,
            user_id=model.user_id,
            token_hash=model.token_hash,
            device_info=model.device_info,
            ip_address=model.ip_address,
            expires_at=model.expires_at,
            revoked=model.revoked,
            created_at=model.created_at
        )

    def _to_model(self, entity: RefreshToken) -> RefreshTokenModel:
        """Convert Domain Entity to SQLAlchemy Model."""
        return RefreshTokenModel(
            id=entity.id,
            user_id=entity.user_id,
            token_hash=entity.token_hash,
            device_info=entity.device_info,
            ip_address=entity.ip_address,
            expires_at=entity.expires_at,
            revoked=entity.revoked,
            created_at=entity.created_at
        )

    async def save(self, token: RefreshToken) -> RefreshToken:
        model = self._to_model(token)
        self.session.add(model)
        await self.session.commit()
        return token

    async def get_by_token_hash(self, token_hash: str) -> Optional[RefreshToken]:
        result = await self.session.execute(
            select(RefreshTokenModel).where(RefreshTokenModel.token_hash == token_hash)
        )
        model = result.scalar_one_or_none()
        if model:
            return self._to_entity(model)
        return None

    async def revoke_all_for_user(self, user_id: uuid.UUID) -> None:
        await self.session.execute(
            update(RefreshTokenModel)
            .where(RefreshTokenModel.user_id == user_id)
            .values(revoked=True)
        )
        await self.session.commit()

    async def revoke_by_id(self, token_id: uuid.UUID) -> None:
        await self.session.execute(
            update(RefreshTokenModel)
            .where(RefreshTokenModel.id == token_id)
            .values(revoked=True)
        )
        await self.session.commit()
