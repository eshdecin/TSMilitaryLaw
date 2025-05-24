from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

class ChatRequest(BaseModel):
    query: str

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
        index = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        result = index.similarity_search(request.query, k=3)
        answer = "\n\n".join([doc.page_content for doc in result])
        return {"message": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
