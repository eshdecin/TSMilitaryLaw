from fastapi import FastAPI
from app.api.routes import router as chat_router

app = FastAPI(title="TSMilitaryLaw Backend")

app.include_router(chat_router, prefix="/chat")
