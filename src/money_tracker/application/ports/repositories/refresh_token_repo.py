from abc import ABC, abstractmethod
from typing import Optional
import uuid
from money_tracker.domain.models.refresh_token import RefreshToken

class RefreshTokenRepository(ABC):
    @abstractmethod
    async def save(self, token: RefreshToken) -> RefreshToken:
        """Save a refresh token to the database."""
        pass

    @abstractmethod
    async def get_by_token_hash(self, token_hash: str) -> Optional[RefreshToken]:
        """Find a refresh token by its hash."""
        pass

    @abstractmethod
    async def revoke_all_for_user(self, user_id: uuid.UUID) -> None:
        """Revoke all refresh tokens for a user (logout from all devices)."""
        pass

    @abstractmethod
    async def revoke_by_id(self, token_id: uuid.UUID) -> None:
        """Revoke a specific refresh token."""
        pass
