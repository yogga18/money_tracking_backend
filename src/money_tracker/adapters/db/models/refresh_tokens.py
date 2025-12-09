from sqlalchemy import Column, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from money_tracker.infrastructure.postgres import Base
import uuid
from datetime import datetime

class RefreshTokenModel(Base):
    __tablename__ = "refresh_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token_hash = Column(String(255), unique=True, nullable=False, index=True)
    device_info = Column(String(255), nullable=True)
    ip_address = Column(String(45), nullable=True)
    expires_at = Column(TIMESTAMP(timezone=True), nullable=False)
    revoked = Column(Boolean, default=False, server_default="false")
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<RefreshTokenModel(id={self.id}, user_id={self.user_id})>"
