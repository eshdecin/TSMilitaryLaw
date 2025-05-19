from fastapi import APIRouter
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings

router = APIRouter()

PDF_DIR = "pdfs"
FAISS_INDEX_PATH = "faiss_index"

@router.get("/rebuild")
def rebuild_index():
    files = [os.path.join(PDF_DIR, f) for f in os.listdir(PDF_DIR) if f.endswith(".pdf")]
    documents = []
    for file in files:
        loader = PyPDFLoader(file)
        documents.extend(loader.load())

    embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
    faiss_index = FAISS.from_documents(documents, embeddings)
    faiss_index.save_local(FAISS_INDEX_PATH)
    
    return {"status": "FAISS index rebuilt successfully", "documents_indexed": len(documents)}
