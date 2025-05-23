from fastapi import FastAPI
from app.api import chat

app = FastAPI()
app.include_router(chat.router)

@app.get("/")
def root():
    return {"message": "Service running. POST to /chat with { query: 'your question' }"}
