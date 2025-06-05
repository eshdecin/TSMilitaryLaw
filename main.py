from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat  # your router

app = FastAPI()

# ✅ FINAL CORS FIX
origins = [
    "https://tsmilitarylaw.info",
    "https://tsmilitarylaw-backend.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Mount the chat router
app.include_router(chat.router)

@app.get("/")
def root():
    return {
        "message": "Service running. POST to /chat with { query: 'your question' }"
    }
