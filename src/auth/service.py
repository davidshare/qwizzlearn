from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from passlib.context import CryptContext

from .schemas import UserCreate
from .models import User
from .utils import generate_password_hash

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:

    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        user = result.first()
        return user

    async def get_user_by_username(self, username: str, session: AsyncSession):
        statement = select(User).where(User.username == username)
        result = await session.exec(statement)
        user = result.first()
        return user

    async def user_exist(self, session: AsyncSession, email: str = None, username: str = None):
        """
        Check if a user exists based on email or username.

        Args:
            session (AsyncSession): The async session to interact with the database.
            email (str): The email of the user to check.
            username (str): The username of the user to check.

        Returns:
            dict: A dictionary containing the existence status of the email and/or username.
        """
        if not email and not username:
            raise ValueError(
                "At least one of `email` or `username` must be provided.")

        result = {}

        if email:
            user_email = await self.get_user_by_email(email, session)
            result['email'] = user_email is not None

        if username:
            user_username = await self.get_user_by_username(username, session)
            result['username'] = user_username is not None

        return result


    async def create_user(self, user: UserCreate, session: AsyncSession) -> User:
        """
        Create a new user in the database.

        Args:
            user (UserCreate): The user data to create the user with.

        Returns:
            User: The newly created user object.
        """
        user_dict = user.model_dump()

        new_user = User(**user_dict)
        new_user.password_hash = generate_password_hash(
            user_dict['password'])
        session.add(new_user)
        await session.commit()
        session.refresh(new_user)
        return new_user
