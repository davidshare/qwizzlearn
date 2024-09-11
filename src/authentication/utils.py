from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
import uuid
import logging

from src.config import Config


passwd_context = CryptContext(
    schemes=['bcrypt']
)

ACCESS_TOKEN_EXPIRY = 3600


def generate_password_hash(passwd: str) -> str:
    pwd_hash = passwd_context.hash(passwd)
    return pwd_hash


def verify_password(password: str, hashed_passwd: str) -> bool:
    return passwd_context.verify(password, hashed_passwd)


def create_access_token(user_data: dict, expiry: timedelta | None = None, refresh: bool = False):
    payload = {}
    payload['user'] = user_data
    payload['jti'] = str(uuid.uuid4())
    payload['refresh'] = refresh
    if expiry:
        payload['exp'] = datetime.now() + expiry
    else:
        payload['exp'] = datetime.now(
        ) + timedelta(seconds=ACCESS_TOKEN_EXPIRY)
    token = jwt.encode(
        payload=payload, key=Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)

    return token


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            jwt=token, key=Config.JWT_SECRET_KEY, algorithms=Config.JWT_ALGORITHM)
        return payload
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None
