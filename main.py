from fastapi import FastAPI
from app.api.routes import chat_router

app = FastAPI(
    title="TSMilitaryLaw Chatbot",
    description="API backend for TSMilitaryLaw intelligent assistant",
    version="1.0.0"
)

# Mount chatbot routes
app.include_router(chat_router, prefix="/api/chat")
