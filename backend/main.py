from fastapi import FastAPI
from auth.routes import router as auth_router
from api.routes import router as api_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(api_router, prefix="/api", tags=["CrewAI"])
