from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat

app = FastAPI()

# Infantry-Grade CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://tsmilitarylaw.info",   # Your live frontend
        "http://localhost:3000"         # Optional: Local testing
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include chat route
app.include_router(chat.router)

@app.get("/")
def root():
    return {"message": "Service running. POST to /chat with { query: 'your question' }"}
