import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import OpenAI
from langchain.chains import RetrievalQA

# Load environment variables
load_dotenv()

def load_qa_chain():
    # Create OpenAI embeddings
    embeddings = OpenAIEmbeddings(
        model="text-embedding-ada-002",
        api_key=os.getenv("OPENAI_API_KEY")
    )

    # Load FAISS index
    db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    retriever = db.as_retriever(search_kwargs={"k": 5})

    # Initialize OpenAI LLM
    llm = OpenAI(temperature=0.0, api_key=os.getenv("OPENAI_API_KEY"))

    # Set up QA chain with source docs enabled
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    return qa_chain
