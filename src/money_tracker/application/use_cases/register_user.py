from passlib.context import CryptContext
from money_tracker.domain.models.user import User
from money_tracker.application.ports.repositories.user_repo import UserRepository
from money_tracker.application.dtos.auth_dto import RegisterUserRequest, UserResponse

# Setup Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class RegisterUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def execute(self, request: RegisterUserRequest) -> UserResponse:
        # 1. Check if email already exists
        existing_user = await self.user_repo.get_by_email(request.email)
        if existing_user:
            raise ValueError("Email already registered")

        # 2. Hash Password
        hashed_password = pwd_context.hash(request.password)

        # 3. Create User Entity
        new_user = User(
            email=request.email,
            password_hash=hashed_password,
            full_name=request.full_name
        )

        # 4. Save to Repository
        saved_user = await self.user_repo.save(new_user)

        # 5. Return Response DTO
        return UserResponse.model_validate(saved_user)
