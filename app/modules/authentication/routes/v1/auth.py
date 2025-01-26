from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.core.exceptions import ValidationException

from ...repositories.user import UserRepository
from ...schemas.user import UserCreate, UserResponse
from ...services.auth import AuthService

auth_router = APIRouter()


@auth_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    user_repository = UserRepository(session)
    auth_service = AuthService(user_repository)

    try:
        return await auth_service.register_user(user_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise ValidationException(
            detail={
                "message": "Validation error",
                "errors": str(e),
                "documentation_url": "https://api.example.com/docs"
            }
        ) from e
