from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from qa_chain import load_qa_chain

chat_router = APIRouter()
qa_chain = load_qa_chain()

class ChatQuery(BaseModel):
    question: str

@chat_router.post("/ask")
async def ask_question(query: ChatQuery):
    try:
        result = qa_chain.run(query.question)
        return {"answer": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
