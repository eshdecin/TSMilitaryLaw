from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from qa_chain import load_qa_chain

# Initialize router
chat_router = APIRouter()

# Load the QA chain once at startup
qa_chain = load_qa_chain()

# Request schema
class QueryRequest(BaseModel):
    query: str

# Response route
@chat_router.post("/query")
async def get_chat_response(request: QueryRequest):
    try:
        result = qa_chain.run(request.query)  # Use .run() if it's a Chain, not a function
        sources = [
            doc.metadata.get("source", "unknown") 
            for doc in getattr(result, "source_documents", [])
        ]
        return {
            "answer": result["result"] if isinstance(result, dict) else result,
            "sources": sources
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {e}")
