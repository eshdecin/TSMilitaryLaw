from langchain.chains import RetrievalQA
from langchain_core.language_models import BaseLanguageModel
from langchain_core.vectorstores import VectorStore

def get_chain(llm: BaseLanguageModel, vectorstore: VectorStore) -> RetrievalQA:
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )
