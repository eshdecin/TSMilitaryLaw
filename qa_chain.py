import os
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from dotenv import load_dotenv

load_dotenv()

def load_qa_chain():
    embeddings = OpenAIEmbeddings(
        model="text-embedding-ada-002",
        api_key=os.getenv("OPENAI_API_KEY")
    )

    db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    retriever = db.as_retriever(search_kwargs={"k": 5})

    llm = OpenAI(temperature=0.0, api_key=os.getenv("OPENAI_API_KEY"))

    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)
    return qa_chain
