from typing import Optional
from sqlmodel import SQLModel, Field, create_engine, Session, Relationship
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime

here = os.path.dirname(os.path.abspath(__file__))
db_filename = "users.db"
db_path = os.path.join(here, db_filename)

DATABASE_URL = f"sqlite:///{db_path}"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True, nullable=False)
    name: str
    password: str 
    sessions: list["UserSession"] = Relationship(back_populates="user")

class UserSession(SQLModel, table=True):
    id: str = Field(primary_key=True) 
    user_id: str = Field(foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="sessions")

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
