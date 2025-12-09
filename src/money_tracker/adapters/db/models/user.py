from sqlalchemy import Column, String, DateTime, Text, Boolean, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from money_tracker.infrastructure.postgres import Base
import uuid
from datetime import datetime

class UserModel(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    picture_url = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, server_default="true", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<UserModel(id={self.id}, email={self.email})>"
