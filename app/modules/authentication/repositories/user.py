from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.exceptions import DuplicateEntryException, NotFoundException

from ..models.token import Token
from ..models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user: User) -> User:
        # Check for duplicate username, email, or phone number
        statement = select(User).where(
            (User.username == user.username)
            | (User.email == user.email)
            | (User.phone_number == user.phone_number)
        )
        existing_user = await self.session.exec(statement)
        existing_user = existing_user.first()

        if existing_user:
            if existing_user.username == user.username:
                raise DuplicateEntryException("Username already exists")
            elif existing_user.email == user.email:
                raise DuplicateEntryException("Email already exists")
            elif existing_user.phone_number == user.phone_number:
                raise DuplicateEntryException("Phone number already exists")

        self.session.add(user)
        await self.session.commit()  # Use await for async commit
        await self.session.refresh(user)  # Use await for async refresh
        return user

    async def get_user_by_username(self, username: str) -> User:
        """
        Retrieve a user from the database by their username using SQLModel.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            User: The User object if found.

        Raises:
            NotFoundException: If no user with the given username exists.
            SQLAlchemyError: If a database error occurs.
        """
        try:
            statement = select(User).where(User.username == username)
            result = await self.session.exec(statement)
            user = result.first()
            return user
        except NotFoundException as e:
            print(f"User '{e}' not found, proceeding with default...")
        except SQLAlchemyError as e:
            print(f"Database error: {e}")

    async def get_token_by_refresh_token(self, refresh_token: str) -> Token:
        """Retrieve a token by its refresh token."""
        statement = select(Token).where(Token.refresh_token == refresh_token)
        result = await self.session.exec(statement)
        token = result.first()
        if not token:
            raise NotFoundException("Refresh token not found")
        return token
