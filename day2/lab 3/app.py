import streamlit as st
import pickle
import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_classic.retrievers import EnsembleRetriever
from langchain_classic.chains import RetrievalQA
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Tech Catalog Hybrid Search", page_icon="🔍", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f7f9fc; }
    .stSelectbox label { font-weight: bold; }
    .chat-bubble { padding: 15px; border-radius: 10px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); color: #000000; }
    .user { background-color: #e0f2fe; border-left: 5px solid #0ea5e9; color: #000000; }
    .ai { background-color: #ffffff; border-left: 5px solid #10b981; color: #000000; }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Configuration")
    groq_api_key = st.text_input("Groq API Key", type="password")
    st.markdown("---")
    st.info("Lab 3: Hybrid Search (BM25 + Chroma) with Metadata filtering.")

st.title("🔍 Tech Catalog Assistant")
st.markdown("Search our product catalog using **Hybrid Search** with metadata filtering!")

# Setup UI filtering
categories = ["All", "Laptops", "Smartphones", "Accessories"]
selected_category = st.selectbox("Select Product Category to Filter:", categories)

@st.cache_resource
def get_retrievers():
    if not os.path.exists("./chroma_db") or not os.path.exists("bm25_retriever.pkl"):
        return None, None
    
    # 1. Load Chroma
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    
    # 2. Load BM25
    with open("bm25_retriever.pkl", "rb") as f:
        bm25_retriever = pickle.load(f)
        
    return vector_db, bm25_retriever

vector_db, bm25_retriever = get_retrievers()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    role = "user" if msg["role"] == "user" else "ai"
    st.markdown(f'<div class="chat-bubble {role}"><strong>{"You" if role == "user" else "AI"}:</strong> {msg["content"]}</div>', unsafe_allow_html=True)

if query := st.chat_input("E.g. What laptops have an OLED display?"):
    if not groq_api_key:
        st.warning("Please provide your Groq API Key.")
        st.stop()
        
    if not vector_db:
        st.error("Databases not found. Run ingest.py first!")
        st.stop()
        
    st.session_state.messages.append({"role": "user", "content": query})
    st.rerun()

if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    query = st.session_state.messages[-1]["content"]
    
    with st.spinner("Searching using Hybrid Retriever..."):
        # Configure Chroma Retriever with Metadata Filter
        search_kwargs = {"k": 2}
        if selected_category != "All":
            search_kwargs["filter"] = {"category": selected_category}
            
        chroma_retriever = vector_db.as_retriever(search_kwargs=search_kwargs)
        
        # NOTE: BM25 in LangChain does not natively support pre-filtering by metadata in its standard 
        # implementation, so it will search over all documents, but Chroma strictly abides by the filter.
        # This demonstrates real-world nuances of combining retrievers.
        bm25_retriever.k = 2
        
        # Combine into Hybrid Retriever (50% weight each)
        ensemble_retriever = EnsembleRetriever(
            retrievers=[bm25_retriever, chroma_retriever],
            weights=[0.5, 0.5]
        )
        
        llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.1-8b-instant", temperature=0)
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=ensemble_retriever,
            return_source_documents=True
        )
        
        try:
            response = qa_chain.invoke({"query": query})
            st.session_state.messages.append({"role": "ai", "content": response["result"]})
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")
