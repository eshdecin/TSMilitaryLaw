from fastapi import FastAPI
from app.api import chat, rebuild  # Import both routers

app = FastAPI()

# Mount API routers
app.include_router(chat.router)
app.include_router(rebuild.router)

@app.get("/")
def root():
    return {
        "message": "Service running. POST to /chat with { query: 'your question' }"
    }
