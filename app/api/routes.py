from fastapi import APIRouter

chat_router = APIRouter()

@chat_router.get("/")
async def root():
    return {"message": "Chatbot backend is ready, Sir!"}
