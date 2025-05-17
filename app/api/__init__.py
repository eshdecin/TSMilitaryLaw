from fastapi import APIRouter
from app.api import chat  # import chat route

router = APIRouter()
router.include_router(chat.router)
