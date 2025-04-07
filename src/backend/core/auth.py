from jose import jwt, JWTError
from passlib.context import CryptContext
from typing import Optional
from config.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---------------------------
# 🔐 PASSWORD UTILS
# ---------------------------

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# ---------------------------
# 🔐 JWT TOKEN UTILS
# ---------------------------

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# ---------------------------
# 🔍 VERIFY / DECODE TOKENS
# ---------------------------

def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None

def get_username_from_token(token: str) -> Optional[str]:
    payload = decode_token(token)
    return payload.get("sub") if payload else None

def get_role_from_token(token: str) -> Optional[str]:
    payload = decode_token(token)
    return payload.get("role") if payload else None
