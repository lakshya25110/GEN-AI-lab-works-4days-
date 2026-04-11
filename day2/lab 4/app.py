import streamlit as st
import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_classic.chains import RetrievalQA
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Multi-Document RAG", page_icon="📚", layout="wide")

st.markdown("""
    <style>
    .chat-bubble, .chat-bubble * { color: #000000 !important; }
    .chat-bubble { padding: 15px; border-radius: 10px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .user { background-color: #e0f2fe; border-left: 5px solid #0ea5e9; }
    .ai { background-color: #ffffff; border-left: 5px solid #8b5cf6; }
    .source-box { font-size: 0.8em; background: #e5e7eb; padding: 5px; border-radius: 5px; display: inline-block; margin-right: 5px; color: #000000 !important;}
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Configuration")
    groq_api_key = st.text_input("Groq API Key", type="password")
    st.markdown("---")
    st.info("Lab 4: Multi-Document RAG\n\nQuerying over:\n- PDF (HR Policy)\n- CSV (Inventory)\n- TXT (Company History)")

st.title("📚 Unified Knowledge AI")
st.markdown("Ask anything regarding HR policies, the TechFlow company history, or the current IT hardware inventory.")

@st.cache_resource
def load_db():
    persist_directory = "./chroma_db"
    if not os.path.exists(persist_directory):
        return None
    
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    return vector_db

vector_db = load_db()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    role_class = "user" if msg["role"] == "user" else "ai"
    st.markdown(f'<div class="chat-bubble {role_class}"><strong>{"You" if role_class == "user" else "AI"}:</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)

if query := st.chat_input("E.g., How much PTO do I get? And who has the ThinkPad T14?"):
    if not groq_api_key:
        st.warning("Please provide your Groq API Key.")
        st.stop()
        
    if not vector_db:
        st.error("Database not found. Run ingest.py first!")
        st.stop()
        
    st.session_state.messages.append({"role": "user", "content": query})
    st.rerun()

if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    query = st.session_state.messages[-1]["content"]
    
    with st.spinner("Searching across PDF, CSV, and TXT files..."):
        llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.1-8b-instant", temperature=0)
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vector_db.as_retriever(search_kwargs={"k": 4}),
            return_source_documents=True
        )
        
        try:
            response = qa_chain.invoke({"query": query})
            answer = response["result"]
            sources = response["source_documents"]
            
            # Format sources for debugging/insight
            source_names = list(set([os.path.basename(doc.metadata.get('source', 'Unknown')) for doc in sources]))
            source_html = "<br><br><strong>Sources utilized:</strong><br>" + "".join([f'<span class="source-box">{s}</span>' for s in source_names])
            
            st.session_state.messages.append({"role": "ai", "content": answer + source_html})
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")
