import os
from fastapi import FastAPI, Request
from pydantic import BaseModel
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA

app = FastAPI()

PDF_DIR = "pdfs"
FAISS_INDEX_PATH = "faiss_index"

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

        return {"status": "success", "message": "FAISS index rebuilt successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/chat")
def chat(request: QueryRequest):
    try:
        print("Loading FAISS index and setting up retriever...")
        embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
        faiss_index = FAISS.load_local(FAISS_INDEX_PATH, embeddings)

        retriever = faiss_index.as_retriever()
        qa_chain = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), temperature=0),
            retriever=retriever
        )

        print(f"Processing query: {request.query}")
        result = qa_chain.run(request.query)
        return {"response": result}

    except Exception as e:
        return {"error": str(e)}

# Optional GET handler for /rebuild (for browsers that send HEAD first)
@app.head("/rebuild")
def rebuild_head():
    return {"status": "ready"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
