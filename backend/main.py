from fastapi import FastAPI
from .auth.routes import router as auth_router
from .api.routes import router as api_router
from fastapi.middleware.cors import CORSMiddleware
from .api.sessions import router as sessions_router

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(sessions_router, prefix="/api", tags=["Sessions"])
app.include_router(api_router, prefix="/api", tags=["CrewAI"])

