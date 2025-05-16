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

        embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
        faiss_index = FAISS.from_documents(documents, embeddings)
        faiss_index.save_local("faiss_index")

        return {"status": "success", "message": "FAISS index rebuilt successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Optional HEAD handler to suppress 405 error
@app.head("/rebuild")
def head_rebuild():
    return {"message": "HEAD request acknowledged. Use GET for actual rebuild."}

# Required to keep Render happy
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
