from fastapi import FastAPI
from app.api.routes import chat_router
import os

app = FastAPI(title="TSMilitaryLaw Backend")

app.include_router(chat_router, prefix="/chat")

# Deployment fix: Use environment-injected port
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
