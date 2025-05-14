from fastapi import FastAPI
from app.api.routes import chat_router

app = FastAPI(
    title="TSMilitaryLaw Chatbot API",
    description="Backend for TSMilitaryLaw chatbot",
    version="1.0.0"
)

# Attach chat endpoints
app.include_router(chat_router, prefix="/api/chat")
