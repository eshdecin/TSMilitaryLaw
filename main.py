from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat
import os
from dotenv import load_dotenv

# Load environment variables from .env (for local dev)
load_dotenv()

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tsmilitarylaw.info"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the chat router
app.include_router(chat.router)

@app.get("/")
def root():
    return {"message": "Service running. POST to /chat with { query: 'your question' }"}
