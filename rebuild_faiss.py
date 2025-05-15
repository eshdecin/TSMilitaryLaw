import os
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings

# Set path to your PDF directory
pdf_dir = "pdfs"
files = [os.path.join(pdf_dir, f) for f in os.listdir(pdf_dir) if f.endswith(".pdf")]

# Load all documents
documents = []
for file in files:
    loader = PyPDFLoader(file)
    documents.extend(loader.load())

# Embed and index
embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
faiss_index = FAISS.from_documents(documents, embeddings)

# Save index to a folder named 'faiss_index'
faiss_index.save_local("faiss_index")
print("FAISS index rebuilt and saved to faiss_index/")
