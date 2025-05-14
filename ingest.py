import os
import glob
import fitz  # PyMuPDF
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from dotenv import load_dotenv

# Load the OpenAI API key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Directory where PDFs are stored
PDF_DIR = "pdfs"

# Output path for FAISS index
DB_PATH = "faiss_index"

def load_and_split_pdfs(directory):
    all_docs = []
    for filepath in glob.glob(os.path.join(directory, "*.pdf")):
        print(f"[+] Loading {filepath}")
        text = ""
        with fitz.open(filepath) as doc:
            for page in doc:
                text += page.get_text()
        metadata = {"source": os.path.basename(filepath)}
        all_docs.append(Document(page_content=text, metadata=metadata))
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.split_documents(all_docs)

def build_vector_store(documents, api_key):
    print("[+] Generating embeddings and building FAISS vector store...")
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    db = FAISS.from_documents(documents, embeddings)
    db.save_local(DB_PATH)
    print("[+] Vector store saved to:", DB_PATH)

if __name__ == "__main__":
    documents = load_and_split_pdfs(PDF_DIR)
    build_vector_store(documents, openai_api_key)
