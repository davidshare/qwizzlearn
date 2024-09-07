from passlib.context import CryptContext


passwd_context = CryptContext(
    schemes=['bcrypt']
)


def generate_password_hash(passwd: str) -> str:
    pwd_hash = passwd_context.hash(passwd)
    return pwd_hash


def verify_password(password: str, hashed_passwd: str) -> bool:
    return passwd_context.verify(password, hashed_passwd)
