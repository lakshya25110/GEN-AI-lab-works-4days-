import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_classic.chains import RetrievalQA
from dotenv import load_dotenv
import os

# Load Environment Variables
load_dotenv()

# Page Configuration
st.set_page_config(page_title="TechFlow FAQ Assistant (Groq)", page_icon="⚡", layout="wide")

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: white;
    }
    .chat-bubble {
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .user-bubble {
        background-color: #1e40af;
        border-right: 5px solid #3b82f6;
    }
    .ai-bubble {
        background-color: #334155;
        border-left: 5px solid #10b981;
    }
    .sidebar .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar for API Key Management
with st.sidebar:
    st.title("⚙️ Configuration")
    groq_api_key = st.text_input("Enter Groq API Key", type="password", help="Get your key from console.groq.com")
    
    st.markdown("---")
    st.header("About Lab 2")
    st.info("RAG Q&A system for TechFlow FAQs.\n\n**Provider:** Groq (⚡ Fast)\n**Embeddings:** Local (HuggingFace)")
    
    if st.button("🧹 Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Application Header
st.title("⚡ TechFlow FAQ AI Assistant")
st.subheader("Powered by Groq & LangChain")
st.markdown("---")

# Initialize Vector DB & LLM
@st.cache_resource
def load_vector_db():
    try:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        persist_directory = "./chroma_db"
        
        if not os.path.exists(persist_directory):
            return None
            
        vector_db = Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings
        )
        return vector_db
    except Exception as e:
        st.error(f"Error loading vector database: {e}")
        return None

# Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    role_class = "user-bubble" if message["role"] == "user" else "ai-bubble"
    st.markdown(f'<div class="chat-bubble {role_class}"><strong>{"You" if message["role"] == "user" else "AI"}:</strong><br>{message["content"]}</div>', unsafe_allow_html=True)

# User Input
if prompt := st.chat_input("Ask a question about company policies..."):
    if not groq_api_key:
        st.warning("Please enter your Groq API Key in the sidebar to proceed.")
    else:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

# Logic to handle the last user message
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    user_query = st.session_state.messages[-1]["content"]
    
    vector_db = load_vector_db()
    
    if vector_db is None:
        st.error("Vector database not found. Please run index_faq.py first!")
    else:
        with st.spinner("Analyzing TechFlow knowledge base..."):
            try:
                # Initialize Groq LLM
                llm = ChatGroq(
                    groq_api_key=groq_api_key,
                    model_name="llama-3.1-8b-instant",
                    temperature=0.1
                )
                
                qa_chain = RetrievalQA.from_chain_type(
                    llm=llm,
                    chain_type="stuff",
                    retriever=vector_db.as_retriever(search_kwargs={"k": 3}),
                    return_source_documents=True
                )
                
                response = qa_chain.invoke({"query": user_query})
                answer = response["result"]
                
                # Add AI response
                st.session_state.messages.append({"role": "assistant", "content": answer})
                st.rerun()
            except Exception as e:
                st.error(f"API Error: {e}")
