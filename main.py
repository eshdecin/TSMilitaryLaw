import os
from fastapi import FastAPI
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Service running. Use /rebuild to trigger FAISS index generation."}

@app.get("/rebuild")
def rebuild_index():
    try:
        print("Step 1: Reading PDFs from 'pdfs/'...")
        pdf_dir = "pdfs"
        files = [os.path.join(pdf_dir, f) for f in os.listdir(pdf_dir) if f.endswith(".pdf")]
        print(f"Step 2: Found {len(files)} PDF(s)")

        documents = []
        for file in files:
            print(f"Step 3: Loading file: {file}")
            loader = PyPDFLoader(file)
            documents.extend(loader.load())

        print("Step 4: Initializing OpenAI Embeddings...")
        embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))

        print("Step 5: Creating FAISS index...")
        faiss_index = FAISS.from_documents(documents, embeddings)

        print("Step 6: Saving FAISS index to disk...")
        faiss_index.save_local("faiss_index")

        print("Step 7: Completed!")
        return {"status": "success", "message": "FAISS index rebuilt successfully."}

    except Exception as e:
        print(f"ERROR: {str(e)}")
        return {"status": "error", "message": str(e)}
