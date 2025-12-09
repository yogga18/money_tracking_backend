from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from money_tracker.adapters.api.dependencies.auth import get_register_use_case, get_login_google_use_case
from money_tracker.application.use_cases.auth.register_user import RegisterUserUseCase
from money_tracker.application.use_cases.auth.login_google import LoginGoogleUseCase
from money_tracker.application.dtos.auth_dto import RegisterUserRequest, UserResponse

router = APIRouter(prefix="/auth", tags=["Auth"])

# DTO for Google Login Request
class GoogleLoginRequest(BaseModel):
    token: str  # Google ID Token from frontend

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterUserRequest,
    use_case: RegisterUserUseCase = Depends(get_register_use_case)
):
    try:
        return await use_case.execute(request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/google")
async def login_google(
    request: GoogleLoginRequest,
    use_case: LoginGoogleUseCase = Depends(get_login_google_use_case)
):
    """Login or Register with Google SSO."""
    try:
        return await use_case.execute(request.token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
