from datetime import datetime
from typing import Optional
import uuid

class User:
    def __init__(
        self, 
        email: str, 
        password_hash: str, 
        full_name: str,
        id: Optional[uuid.UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id or uuid.uuid4()
        self.email = email
        self.password_hash = password_hash
        self.full_name = full_name
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def update_profile(self, full_name: str):
        """Update user's full name and refresh updated_at timestamp."""
        self.full_name = full_name
        self.updated_at = datetime.utcnow()

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
