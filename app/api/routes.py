from fastapi import APIRouter

chat_router = APIRouter()

@chat_router.post("/chat")
async def root(query: dict):
    return {
        "message": f"Received your question: {query['query']} (Real brain coming soon, Sir!)"
    }
