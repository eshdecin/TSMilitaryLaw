from fastapi import APIRouter, Request
from pydantic import BaseModel
from qa_chain import load_qa_chain

chat_router = APIRouter()
qa_chain = load_qa_chain()

class ChatRequest(BaseModel):
    query: str

@chat_router.post("/chat")
async def chat_endpoint(req: ChatRequest):
    try:
        response = qa_chain({"query": req.query})
        answer = response.get("result", "No answer found.")
        return {"message": answer}
    except Exception as e:
        return {"message": f"[!] Error: {str(e)}"}
