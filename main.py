from fastapi import FastAPI
from app.api.routes import chat_router  # Ensure this path matches your file structure

app = FastAPI(
    title="TSMilitaryLaw Chatbot API",
    version="1.0",
    description="Query military law documents via LangChain + OpenAI"
)

# Register routes
app.include_router(chat_router, prefix="/api/chat")
