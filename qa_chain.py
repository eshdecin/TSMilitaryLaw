import os
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA

load_dotenv()

DB_PATH = "faiss_index"

def load_qa_chain():
    # No need to pass API key manually; it uses env variable
    embeddings = OpenAIEmbeddings()
    vectordb = FAISS.load_local(DB_PATH, embeddings, allow_dangerous_deserialization=True)

    retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 5})

    llm = ChatOpenAI(model="gpt-4", temperature=0.3)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )

    return qa_chain
