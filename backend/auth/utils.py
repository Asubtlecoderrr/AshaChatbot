import jwt
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status
from passlib.context import CryptContext
from ..database.models import User
from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from ..database.models import UserSession, get_session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import timezone
import os
from uuid import uuid4
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

http_bearer = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_or_get_session(user_id: int, db: Session) -> str:
    session_id = str(uuid4())
    user_session = UserSession(id=session_id, user_id=user_id)
    db.add(user_session)
    db.commit()
    db.refresh(user_session)
    return session_id

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Creates JWT token with a specific expiration time.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    """
    Verifies a JWT token and returns its decoded data.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer), 
    session: Session = Depends(get_session),
):
    """
    Get current user from the token
    """
    token = credentials.credentials  
    payload = verify_access_token(token)
    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Malformed token")
    
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

