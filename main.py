from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import chat_router

app = FastAPI()

# Pro Tip: Replace "*" with your exact domain for better security
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # This fixes the OPTIONS issue
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/chat")
