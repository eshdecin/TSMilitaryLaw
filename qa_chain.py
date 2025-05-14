import os
from dotenv import load_dotenv
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

load_dotenv()

DB_PATH = "faiss_index"
openai_key = os.getenv("OPENAI_API_KEY")

def load_qa_chain():
    # Load embeddings and vector store
    embeddings = OpenAIEmbeddings(openai_api_key=openai_key)
    vectordb = FAISS.load_local(DB_PATH, embeddings, allow_dangerous_deserialization=True)

    # Create retriever
    retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 5})

    # Load GPT-4 LLM
    llm = ChatOpenAI(openai_api_key=openai_key, model="gpt-4", temperature=0.3)

    # Create QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )

    return qa_chain
