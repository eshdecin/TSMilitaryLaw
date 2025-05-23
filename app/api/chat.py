from fastapi import APIRouter, Request
from pydantic import BaseModel
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
import os

router = APIRouter()

# Define Pydantic model for request body
class ChatRequest(BaseModel):
    query: str

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    query = request.query

    # Load FAISS index
    index = FAISS.load_local("faiss_index", OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY")))

    # Search relevant documents
    docs = index.similarity_search(query)
    content = "\n".join(doc.page_content for doc in docs[:3]) if docs else "No relevant content found."

    # Send to OpenAI LLM
    llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = llm.invoke(f"Based on the following content, answer this: {query}\n\n{content}")
    
    return {"message": response.content}
