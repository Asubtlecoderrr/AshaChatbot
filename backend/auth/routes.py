from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlmodel import Session, select
from passlib.context import CryptContext

from ..database.models import User, get_session
from .utils import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()

# Request bodies for login and registration
class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Response schema for registration
class RegisterResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    message: str

# Response schema for login
class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Registration endpoint (for user sign up)
@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(req: RegisterRequest, session: Session = Depends(get_session)):
    # Hash the password
    hashed_pw = pwd_context.hash(req.password)
    user = User(name=req.name, email=req.email, password=hashed_pw)
    session.add(user)
    try:
        session.commit()
        session.refresh(user)
    except Exception:
        session.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "message": "Registration successful—please log in.",
    }

# Login endpoint (for obtaining JWT token)
@router.post("/login", response_model=LoginResponse)
def login(req: LoginRequest, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == req.email)).first()
    if not user or not pwd_context.verify(req.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Issue JWT token
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token}
