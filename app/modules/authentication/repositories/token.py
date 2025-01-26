from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.exceptions import NotFoundException
from ..models.token import Token


class TokenRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_token(self, token: Token) -> Token:
        """Create a new token."""
        self.session.add(token)
        await self.session.commit()
        await self.session.refresh(token)
        return token

    async def get_token_by_refresh_token(self, refresh_token: str) -> Token:
        """Retrieve a token by its refresh token."""
        statement = select(Token).where(Token.refresh_token == refresh_token)
        result = await self.session.exec(statement)
        token = result.first()
        if not token:
            raise NotFoundException("Refresh token not found")
        return token

    async def revoke_token(self, refresh_token: str) -> None:
        """Revoke a token by marking it as revoked."""
        token = await self.get_token_by_refresh_token(refresh_token)
        token.revoked = True
        await self.session.commit()
