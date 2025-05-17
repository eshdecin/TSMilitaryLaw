from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from qa_chain import get_chain  # If you have this file, otherwise I'll update

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
        raise HTTPException(status_code=404, detail="FAISS index not found. Please rebuild it first.")

    embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
    vectorstore = FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)

    docs = vectorstore.similarity_search(query)
    chain = load_qa_chain(ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), temperature=0), chain_type="stuff")
    response = chain.run(input_documents=docs, question=query)

    return {"response": response}
