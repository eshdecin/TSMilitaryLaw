from fastapi import APIRouter, Request
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

router = APIRouter()

@router.post("/chat")
async def chat_endpoint(request: Request):
    body = await request.json()
    query = body.get("query")

    if not query:
        return {"message": "Query field is required."}

    # Fix: Allow trusted deserialization
    index = FAISS.load_local(
        "faiss_index",
        OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY")),
        allow_dangerous_deserialization=True
    )

    retriever = index.as_retriever(search_kwargs={"k": 5})
    docs = retriever.get_relevant_documents(query)
    
    content = "\n---\n".join([doc.page_content for doc in docs])
    return {"message": content or "No relevant content found."}
