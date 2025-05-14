from fastapi import FastAPI
from app.api.routes import chat_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="TSMilitaryLaw Backend")

# CORS fix
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/chat")
