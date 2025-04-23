import jwt
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status
from passlib.context import CryptContext
from ..database.models import User
from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from ..database.models import get_session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import timezone
import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# HTTPBearer is used to get the token from the request
http_bearer = HTTPBearer()

# Setup CryptContext (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
    
    # Create the JWT token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    """
    Verifies a JWT token and returns its decoded data.
    """
    try:
        # Decode the JWT token to get the payload
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Return the decoded token data
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),  # Token extracted from the Authorization header
    session: Session = Depends(get_session),
):
    """
    Get current user from the token
    """
    token = credentials.credentials  # Extract the token from the credentials
    payload = verify_access_token(token)
    email = payload.get("sub")  # Extract email from the token payload
    if not email:
        raise HTTPException(status_code=401, detail="Malformed token")
    
    # Fetch the user from the database using the email extracted from the token
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user
