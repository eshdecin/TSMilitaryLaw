from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.qa_chain import load_qa_chain

# Initialize router and QA chain
chat_router = APIRouter()
qa_chain = load_qa_chain()

# Request schema
class QueryRequest(BaseModel):
    query: str

# Route for processing queries
@chat_router.post("/query")
async def get_chat_response(request: QueryRequest):
    try:
        result = qa_chain(request.query)
        return {
            "answer": result["result"],
            "sources": [doc.metadata.get("source") for doc in result.get("source_documents", [])]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
