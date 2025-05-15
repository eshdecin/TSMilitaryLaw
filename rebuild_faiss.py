import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

def rebuild_faiss():
    docs_path = "docs"  # folder containing your PDFs
    all_documents = []

    for filename in os.listdir(docs_path):
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(docs_path, filename))
            all_documents.extend(loader.load())

    # Split text into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(all_documents)

    # Create embeddings
    embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))

    # Build FAISS and save
    faiss_index = FAISS.from_documents(docs, embeddings)
    faiss_index.save_local("faiss_index")

if __name__ == "__main__":
    rebuild_faiss()
    print("FAISS index rebuilt successfully.")
