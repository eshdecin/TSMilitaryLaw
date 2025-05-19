from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from qa_chain import get_chain
import os

router = APIRouter()

PDF_DIR = "pdfs"
FAISS_INDEX_PATH = "faiss_index"

class ChatRequest(BaseModel):
    query: str

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    query = request.query

    if not os.path.exists(FAISS_INDEX_PATH):
        raise HTTPException(status_code=404, detail="FAISS index not found. Please run /rebuild.")

    embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
    vectorstore = FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)

    docs = vectorstore.similarity_search(query)
    chain = get_chain(ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), temperature=0.3))
    response = chain.run(input_documents=docs, question=query)

    print("Response from chain:", response)
    return {"message": str(response)}
