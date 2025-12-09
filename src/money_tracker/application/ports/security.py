from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from datetime import timedelta

class UserInfo(ABC):
    email: str
    username: str
    picture: Optional[str] = None
    is_verified: bool = False

class IdentityProvider(ABC):
    @abstractmethod
    async def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify the token with the provider and return user info dict."""
        pass

class TokenProvider(ABC):
    @abstractmethod
    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create a new access token."""
        pass
    
    @abstractmethod
    def create_refresh_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create a new refresh token."""
        pass
