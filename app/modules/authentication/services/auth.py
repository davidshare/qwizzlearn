from app.core.security import hash_password
from app.core.exceptions import InternalServerException
from ..models.user import User
from ..repositories.user import UserRepository
from ..schemas.user import UserCreate, UserResponse


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register_user(self, user_data: UserCreate) -> UserResponse:
        try:
            # Hash the password
            hashed_password = hash_password(user_data.password)

            # Create the user object
            user = User(
                username=user_data.username,
                email=user_data.email,
                phone_number=user_data.phone_number,
                password_hash=hashed_password,
            )

            # Save the user to the database asynchronously
            created_user = await self.user_repository.create_user(user)

            # Return the user response
            return UserResponse.model_validate(created_user)
        except Exception as e:
            raise InternalServerException(
                f"An error occurred: {str(e)}") from e
