from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.authorisation.dependencies import route_with_action
from src.authorisation.schemas import UserRolesResponse
from src.db.main import get_session

from .controller import AuthenticationController
from .dependencies import (
    AccessTokenBearer, RefreshTokenBearer, get_current_user)
from .schemas import UserCreate, UserLogin, UserRead

authentication_router = APIRouter()


@authentication_router.post("/register", status_code=status.HTTP_201_CREATED,
                            response_model=UserRead)
async def register(user: UserCreate, session: AsyncSession = Depends(get_session)):
    """
    Register a new user.

    Args:
        user (UserCreate): User details including username, email, phone, and password.
        session (AsyncSession): The database session to use for the operation.

    Returns:
        UserRead: The registered user details including id, username, email,
                email verification status, and timestamps.
    """
    return await AuthenticationController.register(user, session)


@authentication_router.post("/login", status_code=status.HTTP_200_OK,
                            response_model=UserRead)
async def login(login_data: UserLogin, session: AsyncSession = Depends(get_session)):
    """
    Log in a user and return user details.

    Args:
        login_data (UserLogin): Email and password of the user.
        session (AsyncSession): The database session to use for the operation.

    Returns:
        UserRead: The user details including id, username, email, email
                verification status, and timestamps.
    """
    return await AuthenticationController.login(login_data, session)


@authentication_router.get("/refresh-token")
async def refresh_token(token_details: dict = Depends(RefreshTokenBearer())):
    """
    Refresh the authentication token.

    Args:
        token_details (dict): Details of the refresh token provided by the 
            RefreshTokenBearer dependency.

    Returns:
        dict: A dictionary containing the new access and refresh tokens.
    """
    return AuthenticationController.refresh_token(token_details)


@authentication_router.get("/me")
@route_with_action("get_current_user")
async def current_user(user=Depends(get_current_user)):
    """
    Retrieve the current user's details.

    Args:
        user: The current user obtained from the get_current_user dependency.

    Returns:
        UserRead: The details of the currently authenticated user.
    """
    return user


@authentication_router.get("/roles", response_model=UserRolesResponse)
async def get_user_roles(session: AsyncSession = Depends(get_session)):
    """
    Retrieve the roles for a specific user. The user ID is hardcoded for testing purposes.

    Args:
        session (AsyncSession): The database session to use for the operation.

    Returns:
        UserRolesResponse: A list of roles represented as dictionaries.
    """
    user_id = 1  # Hardcoded user ID for testing
    try:
        roles = await AuthenticationController.get_user_roles(user_id, session)
        return UserRolesResponse(user_id=user_id, roles=roles)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) from e


@authentication_router.get("/logout")
async def logout(token_details: dict = Depends(AccessTokenBearer())):
    """
    Log out the current user by invalidating their access token.

    Args:
        token_details (dict): Details of the access token from the AccessTokenBearer dependency.

    Returns:
        dict: A confirmation message or status indicating the logout result.
    """
    return await AuthenticationController.logout(token_details)
