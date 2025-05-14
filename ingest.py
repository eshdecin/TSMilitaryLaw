import os
from langchain.document_loaders import (
    PyPDFLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredPowerPointLoader,
    UnstructuredExcelLoader,
    TextLoader
)
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = "./pdfs"

def load_documents():
    documents = []

    for filename in os.listdir(DATA_DIR):
        filepath = os.path.join(DATA_DIR, filename)
        ext = filename.split(".")[-1].lower()

        try:
            if ext == "pdf":
                documents.extend(PyPDFLoader(filepath).load())
            elif ext == "docx":
                documents.extend(UnstructuredWordDocumentLoader(filepath).load())
            elif ext == "pptx":
                documents.extend(UnstructuredPowerPointLoader(filepath).load())
            elif ext in ["xlsx", "xls"]:
                documents.extend(UnstructuredExcelLoader(filepath).load())
            elif ext == "txt":
                documents.extend(TextLoader(filepath).load())
            else:
                print(f"Unsupported file type skipped: {filename}")
        except Exception as e:
            print(f"Error loading {filename}: {e}")

    return documents

def build_vector_store(docs):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local("faiss_index")

if __name__ == "__main__":
    docs = load_documents()
    print(f"Loaded {len(docs)} documents")
    build_vector_store(docs)
    print("FAISS vectorstore created and saved.")
