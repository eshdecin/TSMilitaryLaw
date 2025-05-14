import os
from PyPDF2 import PdfReader
import docx2txt
from pptx import Presentation
import pandas as pd

from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()
DATA_DIR = "pdfs"  # folder containing all legal docs
DB_PATH = "faiss_index"
openai_key = os.getenv("OPENAI_API_KEY")


def extract_text_from_file(filepath):
    ext = filepath.split(".")[-1].lower()
    text = ""

    try:
        if ext == "pdf":
            reader = PdfReader(filepath)
            for page in reader.pages:
                text += page.extract_text() + "\n"

        elif ext == "docx":
            text = docx2txt.process(filepath)

        elif ext == "txt":
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()

        elif ext == "pptx":
            prs = Presentation(filepath)
            for slide in prs.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        text += shape.text + "\n"

        elif ext in ["xlsx", "xls"]:
            df = pd.read_excel(filepath, sheet_name=None)
            for sheet, data in df.items():
                text += data.to_string(index=False) + "\n"

        else:
            print(f"[-] Skipping unsupported format: {filepath}")

    except Exception as e:
        print(f"[!] Error loading {filepath}: {e}")

    return text


def load_documents():
    documents = []
    for filename in os.listdir(DATA_DIR):
        filepath = os.path.join(DATA_DIR, filename)
        text = extract_text_from_file(filepath)
        if text.strip():
            documents.append(Document(page_content=text, metadata={"source": filename}))
    return documents


def build_vector_store(documents):
    print("[+] Building FAISS vector store...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(openai_api_key=openai_key)
    db = FAISS.from_documents(split_docs, embeddings)
    db.save_local(DB_PATH)
    print("[+] Vector store saved to", DB_PATH)


if __name__ == "__main__":
    docs = load_documents()
    print(f"[+] Loaded {len(docs)} files.")
    build_vector_store(docs)
