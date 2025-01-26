from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID
from app.core.exceptions import NotFoundException
from ..models.session import Session


class SessionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_session(self, session: Session) -> Session:
        """Create a new session."""
        self.session.add(session)
        await self.session.commit()
        await self.session.refresh(session)
        return session

    async def get_session_by_token(self, session_token: str) -> Session:
        """Retrieve a session by its token."""
        statement = select(Session).where(
            Session.session_token == session_token)
        result = await self.session.exec(statement)
        session = result.first()
        if not session:
            raise NotFoundException("Session not found")
        return session

    async def delete_session(self, session_token: str) -> None:
        """Delete a session by its token."""
        session = await self.get_session_by_token(session_token)
        await self.session.delete(session)
        await self.session.commit()
