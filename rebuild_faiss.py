import os
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings

# Directory where your reference PDFs are stored
PDF_DIR = "pdfs"

def load_documents():
    docs = []
    for filename in os.listdir(PDF_DIR):
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(PDF_DIR, filename))
            docs.extend(loader.load())
    return docs

def build_faiss_index():
    documents = load_documents()
    print(f"Loaded {len(documents)} documents.")
    embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
    db = FAISS.from_documents(documents, embeddings)
    db.save_local("faiss_index")
    print("FAISS index created and saved to 'faiss_index/'.")

if __name__ == "__main__":
    build_faiss_index()
