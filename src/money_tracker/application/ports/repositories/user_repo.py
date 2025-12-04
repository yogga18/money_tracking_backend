from abc import ABC, abstractmethod
from typing import Optional
import uuid
from money_tracker.domain.models.user import User

class UserRepository(ABC):
    @abstractmethod
    async def save(self, user: User) -> User:
        """Save a user to the database (Create or Update)."""
        pass

    @abstractmethod
    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """Retrieve a user by their unique ID."""
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by their email address."""
        pass
