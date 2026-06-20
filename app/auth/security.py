from datetime import UTC, datetime,timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from fastapi import Depends, HTTPException

SECRET_KEY="stock_exchange_secret"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60

from passlib.context import CryptContext
pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_access_token(data):
    payload=data.copy()
    expire=datetime.now(UTC)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id=payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )