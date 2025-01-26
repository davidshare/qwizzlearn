from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError


async def validation_exception_handler(request: Request, exc: ValidationError):
    errors = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"])
        errors.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"],
        })
    return JSONResponse(
        status_code=422,
        content={
            "message": "Validation error",
            "errors": errors,
            "documentation_url": "https://api.example.com/docs"
        },
    )


async def duplicate_entry_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=409,
        content={
            "message": "Duplicate entry",
            "detail": exc.detail,
            "documentation_url": "https://api.example.com/docs"
        },
    )


async def internal_server_error_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal server error",
            "detail": exc.detail,
            "documentation_url": "https://api.example.com/docs"
        },
    )
