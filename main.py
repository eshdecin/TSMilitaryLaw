from fastapi import FastAPI
from app.api import router as api_router
from pydantic import BaseModel
import os
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader

PDF_DIR = "pdfs"
FAISS_INDEX_PATH = "faiss_index"

app = FastAPI()

# Mount internal API routes
app.include_router(api_router)

class QueryRequest(BaseModel):
    query: str

@app.get("/")
def root():
    return {"message": "Service running. Use /rebuild to trigger FAISS index generation."}

@app.get("/rebuild")
def rebuild_index():
    try:
        print("Step 1: Reading PDFs from 'pdfs/'...")
        files = [os.path.join(PDF_DIR, f) for f in os.listdir(PDF_DIR) if f.endswith(".pdf")]
        print(f"Step 2: Found {len(files)} PDF(s)")

        documents = []
        for file in files:
            print(f"Step 3: Loading file: {file}")
            loader = PyPDFLoader(file)
            documents.extend(loader.load())

        embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
        faiss_index = FAISS.from_documents(documents, embeddings)
        faiss_index.save_local(FAISS_INDEX_PATH)
        return {"message": f"FAISS index rebuilt from {len(files)} PDF(s)"}
    except Exception as e:
        return {"error": str(e)}
