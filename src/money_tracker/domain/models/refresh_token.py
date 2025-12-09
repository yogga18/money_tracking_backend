from datetime import datetime
from typing import Optional
import uuid

class RefreshToken:
    def __init__(
        self,
        token_hash: str,
        user_id: uuid.UUID,
        expires_at: datetime,
        id: Optional[uuid.UUID] = None,
        device_info: Optional[str] = None,
        ip_address: Optional[str] = None,
        revoked: bool = False,
        created_at: Optional[datetime] = None
    ):
        self.id = id or uuid.uuid4()
        self.user_id = user_id
        self.token_hash = token_hash
        self.device_info = device_info
        self.ip_address = ip_address
        self.expires_at = expires_at
        self.revoked = revoked
        self.created_at = created_at or datetime.utcnow()

    def revoke(self):
        """Mark token as revoked."""
        self.revoked = True

    def is_expired(self) -> bool:
        """Check if token is expired."""
        return datetime.utcnow() > self.expires_at

    def __repr__(self):
        return f"<RefreshToken(id={self.id}, user_id={self.user_id}, revoked={self.revoked})>"
