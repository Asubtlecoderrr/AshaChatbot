from typing import Optional
from sqlmodel import SQLModel, Field, create_engine, Session
from sqlalchemy.orm import sessionmaker
import os
# 1) Engine
here = os.path.dirname(os.path.abspath(__file__))
db_filename = "users.db"
db_path = os.path.join(here, db_filename)

# SQLite URL that points to `<same folder>/users.db`
DATABASE_URL = f"sqlite:///{db_path}"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2) Models
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True, nullable=False)
    name: str
    password: str  # store your bcrypt-hashed pw here

class CareerInfo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    cohort: Optional[str]
    skills: Optional[str]
    location: Optional[str]
    experience: Optional[str]
    intent: Optional[str]

# 3) Create all tables
def init_db():
    SQLModel.metadata.create_all(engine)

# 4) Dependency for FastAPI routes
def get_session():
    with Session(engine) as session:
        yield session


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
