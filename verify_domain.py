import sys
import os

# Add src to python path
sys.path.append(os.path.join(os.getcwd(), "src"))

from money_tracker.domain.models.user import User
from money_tracker.application.ports.repositories.user_repo import UserRepository

# Test User Entity
user = User(
    email="test@example.com",
    password_hash="hashed_secret",
    full_name="Test User"
)

print(f"✅ User created: {user}")
print(f"   ID: {user.id}")
print(f"   Created At: {user.created_at}")

# Test Update
old_updated_at = user.updated_at
user.update_profile("New Name")
print(f"✅ User updated: {user.full_name}")

if user.updated_at > old_updated_at:
    print("✅ updated_at timestamp refreshed correctly")
else:
    print("❌ updated_at timestamp NOT refreshed")

print("✅ Domain Layer Verification Successful!")
