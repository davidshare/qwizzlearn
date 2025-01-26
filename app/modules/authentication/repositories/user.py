from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.exceptions import DuplicateEntryException
from ..models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user: User) -> User:
        # Check for duplicate username, email, or phone number
        statement = select(User).where(
            (User.username == user.username) |
            (User.email == user.email) |
            (User.phone_number == user.phone_number)
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
