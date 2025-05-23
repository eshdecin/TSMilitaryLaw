from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat

app = FastAPI()

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tsmilitarylaw.info"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include chat router
app.include_router(chat.router)

@app.get("/")
def root():
    return {"message": "Service running. POST to /chat with { query: 'your question' }"}
