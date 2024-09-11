from typing import Dict, List, Optional

from passlib.context import CryptContext
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.authorisation.models import Role, UserRoles
from src.authorisation.schemas import RoleResponse

from .models import User
from .schemas import UserCreate
from .utils import generate_password_hash

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthenticationService:
    """
        Class to handle authentication
    """

    async def get_user_by_email(self, email: str, session: AsyncSession) -> Optional[User]:
        """
        Fetch a user by their email address.
        :param email: Email address of the user.
        :param session: Async SQLModel session.
        :return: The user if found, or None.
        """
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        user = result.first()
        return user

    async def get_user_by_username(self, username: str, session: AsyncSession) -> Optional[User]:
        """
        Fetch a user by their username.
        :param username: Username of the user.
        :param session: Async SQLModel session.
        :return: The user if found, or None.
        """
        statement = select(User).where(User.username == username)
        result = await session.exec(statement)
        user = result.first()
        return user

    async def user_exist(self, session: AsyncSession, email: Optional[str] = None, username: Optional[str] = None) -> Dict[str, bool]:
        """
        Check if a user exists by email or username.
        :param session: Async SQLModel session.
        :param email: Email address (optional).
        :param username: Username (optional).
        :return: A dictionary indicating if the user exists by email or username.
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

    async def create_user(self, user_data: UserCreate, session: AsyncSession) -> User:
        """
        Create a new user.
        :param user: Data required to create the user (from UserCreate schema).
        :param session: Async SQLModel session.
        :return: The newly created user.
        """
        user_dict = user_data.model_dump()
        new_user = User(**user_dict)
        new_user.password_hash = generate_password_hash(user_dict['password'])

        try:
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
        except Exception as e:
            await session.rollback()
            raise e

        if new_user.roles is None:
            new_user.roles = []
        return new_user

    async def get_user_roles(self, user_id: int, session: AsyncSession) -> List[RoleResponse]:
        """
        Fetch all roles associated with a given user ID, including role details.

        Args:
            user_id (int): ID of the user.
            session (AsyncSession): Async SQLModel session.

        Returns:
            List[RoleResponse]: A list of roles associated with the user.
        """
        if not user_id:
            raise ValueError("Please provide a valid user id")

        # Join UserRoles with Role to get role details
        statement = select(Role).join(UserRoles).where(
            UserRoles.user_id == user_id)
        result = await session.exec(statement)
        roles = result.all()

        return [RoleResponse.model_validate(role) for role in roles]
