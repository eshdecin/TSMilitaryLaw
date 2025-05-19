from fastapi import FastAPI
from app.api.chat import router as chat_router  # Import router directly

app = FastAPI()
app.include_router(chat_router)

@app.get("/")
def root():
    return {
        "message": "Service running. POST to /chat with { query: 'your question' }"
    }
