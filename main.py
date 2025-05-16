import os
import time
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
        start_time = time.time()
        pdf_dir = "pdfs"
        files = [os.path.join(pdf_dir, f) for f in os.listdir(pdf_dir) if f.endswith(".pdf")]

        if not files:
            return {"status": "error", "message": "No PDF files found in /pdfs directory."}

        print(f"Step 1: Found {len(files)} PDF(s)")

        documents = []
        for idx, file in enumerate(files):
            print(f"Step 2.{idx+1}: Loading file: {file}")
            loader = PyPDFLoader(file)
            pages = loader.load()
            if not pages:
                print(f"Warning: No pages loaded from {file}")
            else:
                print(f"Loaded {len(pages)} page(s) from {file}")
                documents.extend(pages)

        if not documents:
            return {"status": "error", "message": "No text extracted from any PDFs."}

        print("Step 3: Initializing embeddings...")
        embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))

        print("Step 4: Generating FAISS index...")
        faiss_index = FAISS.from_documents(documents, embeddings)
        faiss_index.save_local("faiss_index")

        total_time = round(time.time() - start_time, 2)
        print(f"Step 5: FAISS index saved. Total time: {total_time} seconds")

        return {"status": "success", "message": f"FAISS index built in {total_time} seconds with {len(documents)} chunks."}

    except Exception as e:
        print("Exception occurred:", str(e))
        return {"status": "error", "message": str(e)}
       
        if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
