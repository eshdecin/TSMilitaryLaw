import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

# Load environment variables from .env or Render dashboard
load_dotenv()

def load_qa_chain():
    # Initialize OpenAI Embeddings (securely using env variable)
    embeddings = OpenAIEmbeddings(
        model="text-embedding-ada-002",
        api_key=os.getenv("OPENAI_API_KEY")
    )

    # Load FAISS vector store (ensure folder 'faiss_index/' is in root)
    db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

    # Configure the retriever
    retriever = db.as_retriever(search_kwargs={"k": 5})

    # Set up LLM (using OpenAI completion model)
    llm = OpenAI(temperature=0.0, api_key=os.getenv("OPENAI_API_KEY"))

    # Build and return the QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
    return qa_chain
