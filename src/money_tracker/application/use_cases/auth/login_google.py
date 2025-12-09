from typing import Optional
from datetime import datetime, timedelta
import hashlib
from money_tracker.application.ports.security import IdentityProvider, TokenProvider
from money_tracker.application.ports.repositories.user_repo import UserRepository
from money_tracker.application.ports.repositories.refresh_token_repo import RefreshTokenRepository
from money_tracker.domain.models.user import User
from money_tracker.domain.models.refresh_token import RefreshToken
from money_tracker.application.dtos.auth_dto import UserResponse
from money_tracker.core.config import get_settings

settings = get_settings()

class LoginGoogleUseCase:
    def __init__(
        self,
        identity_provider: IdentityProvider,
        token_provider: TokenProvider,
        user_repo: UserRepository,
        refresh_token_repo: RefreshTokenRepository
    ):
        self.identity_provider = identity_provider
        self.token_provider = token_provider
        self.user_repo = user_repo
        self.refresh_token_repo = refresh_token_repo

    async def execute(self, google_token: str, device_info: Optional[str] = None, ip_address: Optional[str] = None) -> dict:
        # 1. Verify Google Token
        user_info = await self.identity_provider.verify_token(google_token)
        
        # 2. Find or Create User
        existing_user = await self.user_repo.get_by_email(user_info["email"])
        
        if existing_user:
            user = existing_user
        else:
            # Create new user from Google info
            new_user = User(
                email=user_info["email"],
                password_hash="",  # No password for SSO users
                full_name=user_info.get("full_name") or user_info["email"].split("@")[0],
                picture_url=user_info.get("picture"),
                is_active=True
            )
            user = await self.user_repo.save(new_user)
        
        # 3. Generate Tokens
        token_data = {"sub": str(user.id), "email": user.email}
        access_token = self.token_provider.create_access_token(token_data)
        refresh_token_jwt = self.token_provider.create_refresh_token(token_data)
        
        # 4. Save Refresh Token to Database
        token_hash = hashlib.sha256(refresh_token_jwt.encode()).hexdigest()
        expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        
        refresh_token_entity = RefreshToken(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=expires_at,
            device_info=device_info,
            ip_address=ip_address
        )
        await self.refresh_token_repo.save(refresh_token_entity)
        
        # 5. Return Response
        return {
            "access_token": access_token,
            "refresh_token": refresh_token_jwt,
            "token_type": "bearer",
            "user": UserResponse.model_validate(user)
        }
