from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

try:
    password = "securepassword"
    print(f"Hashing password: '{password}' (len={len(password)})")
    hashed = pwd_context.hash(password)
    print(f"Success: {hashed}")
except Exception as e:
    print(f"Error: {e}")
