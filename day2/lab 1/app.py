import streamlit as st
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_classic.chains import RetrievalQA
from dotenv import load_dotenv
import os

load_dotenv()

st.title("Nebula-7 Product Manual Q&A")

persist_directory = "./chroma_db"

@st.cache_resource
def load_db():
    if not os.path.exists(persist_directory):
        return None
    embeddings = OpenAIEmbeddings()
    vector_db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    return vector_db

vector_db = load_db()

if vector_db is None:
    st.error("Vector database not found. Please run indexing first.")
else:
    llm = ChatOpenAI(temperature=0)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_db.as_retriever(),
        return_source_documents=False
    )
    
    query = st.text_input("Ask a question about the Nebula-7 drone:")
    if query:
        with st.spinner("Searching..."):
            result = qa_chain.invoke({"query": query})
            st.write(result["result"])
