File: qa_chain.py

import os from dotenv import load_dotenv from langchain.vectorstores import FAISS from langchain_openai import OpenAIEmbeddings  # Updated import from langchain.chat_models import ChatOpenAI from langchain.chains import RetrievalQA

load_dotenv()

DB_PATH = "faiss_index" openai_key = os.getenv("OPENAI_API_KEY")

def load_qa_chain(): embeddings = OpenAIEmbeddings(openai_api_key=openai_key) vectordb = FAISS.load_local(DB_PATH, embeddings, allow_dangerous_deserialization=True)

retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 5})
llm = ChatOpenAI(openai_api_key=openai_key, model="gpt-4", temperature=0.3)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

return qa_chain
