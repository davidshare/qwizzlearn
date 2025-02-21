from typing import Union, Dict, Any
from fastapi import HTTPException, status


class AppException(HTTPException):
    """Base exception class for application-specific errors."""

    def __init__(self, status_code: int, detail: Union[str, Dict[str, Any]]):
        super().__init__(status_code=status_code, detail=detail)


class DuplicateEntryException(AppException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class ValidationException(AppException):
    def __init__(self, detail: Union[str, Dict[str, Any]]):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail
        )


class InternalServerException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )


class UnauthorizedException(HTTPException):
    """Raised when authentication or authorization fails."""

    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class NotFoundException(HTTPException):
    """Raised when a resource is not found."""

    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
