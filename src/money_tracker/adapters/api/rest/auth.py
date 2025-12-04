from fastapi import APIRouter, Depends, HTTPException, status

from money_tracker.adapters.api.dependencies import get_register_use_case
from money_tracker.application.use_cases.register_user import RegisterUserUseCase
from money_tracker.application.dtos.auth_dto import RegisterUserRequest, UserResponse

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterUserRequest,
    use_case: RegisterUserUseCase = Depends(get_register_use_case)
):
    try:
        return await use_case.execute(request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
