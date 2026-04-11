import streamlit as st
import asyncio
import os
import json
from agents_logic import setup_agents_client, run_study_agent
from tools import get_all_progress_data, STATE_FILE, NOTES_DIR

# --- UI Setup ---
st.set_page_config(page_title="Study Assistant | AI Architect", page_icon="📚", layout="wide")

# Premium Dark Aesthetics
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #1a1c24 !important;
        border-right: 1px solid #2d2f39;
    }
    
    /* Progress Cards */
    .progress-card {
        padding: 18px;
        border-radius: 12px;
        background: #252833;
        border: 1px solid #3d4150;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        margin-bottom: 12px;
        transition: transform 0.2s;
    }
    .progress-card:hover {
        transform: translateY(-2px);
        background: #2d313d;
    }
    
    /* Chat Styling */
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
    }
    
    /* Headings */
    h1, h2, h3 {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background: #2e6ff2 !important;
        color: white !important;
        border: none !important;
        font-weight: 600;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background: #4a86ff !important;
        box-shadow: 0 0 15px rgba(46, 111, 242, 0.4);
    }
    
    /* Inputs */
    .stTextInput>div>div>input {
        background-color: #1a1c24 !important;
        color: white !important;
        border: 1px solid #3d4150 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for agent memory
if "agent_history" not in st.session_state:
    st.session_state.agent_history = []

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar: Configuration ---
with st.sidebar:
    st.title("⚙️ AI Control Center")
    
    provider = st.radio("Intelligence Provider", ["Groq", "OpenAI"], index=0)
    
    if provider == "Groq":
        api_key = st.text_input("Groq API Key", type="password", value=os.environ.get("GROQ_API_KEY", ""))
        model = st.selectbox("Model", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"], index=0)
    else:
        default_openai = ""
        api_key = st.text_input("OpenAI API Key", type="password", value=os.environ.get("OPENAI_API_KEY", default_openai))
        model = st.selectbox("Model", ["gpt-4o", "gpt-4o-mini"], index=1)

    tavily_api_key = st.text_input("Tavily API Key (Search)", type="password", value=os.environ.get("TAVILY_API_KEY", ""))
    
    if api_key:
        if provider == "Groq":
            os.environ["GROQ_API_KEY"] = api_key
        else:
            os.environ["OPENAI_API_KEY"] = api_key
            
        setup_agents_client(api_key, provider=provider)
            
    if tavily_api_key:
        os.environ["TAVILY_API_KEY"] = tavily_api_key
        
    st.divider()
    st.subheader("📋 Study Dashboard")
    
    progress_data = get_all_progress_data()
    if progress_data.get("topics"):
        for topic in progress_data["topics"]:
            status_color = "🟢" if topic["status"] == "Completed" else "🟡" if topic["status"] == "In Progress" else "⚪"
            st.markdown(f"""
                <div class="progress-card">
                    <span style='font-size: 1.1rem;'>{status_color} <b>{topic['name']}</b></span><br/>
                    <span style='color: #8a8d97; font-size: 0.85rem;'>{topic.get('timeframe', 'No timeframe set')}</span><br/>
                    <span style='color: #2e6ff2; font-size: 0.85rem;'>Status: {topic['status']}</span>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Your study plan is empty. Ask the architect to build one!")

    if st.button("Reset Session & Progress"):
        if os.path.exists(STATE_FILE):
            os.remove(STATE_FILE)
        st.session_state.agent_history = []
        st.session_state.messages = []
        st.rerun()

# --- Main Interface ---
st.title("📚 Study Assistant: AI Architect")
st.markdown("---")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Welcome Message
if not st.session_state.messages:
    # Add a welcoming architect message
    welcome_text = "👋 Hello! I am your **Senior AI Study Architect**. I am here to design your learning journey and solve any academic doubts you may have using your notes and the web. How can I assist you today?"
    st.session_state.messages.append({"role": "assistant", "content": welcome_text})
    with st.chat_message("assistant"):
        st.markdown(welcome_text)

# Chat input
if prompt := st.chat_input("What's on your mind?"):
    if not api_key:
        st.error(f"Please provide an {provider} API Key in the sidebar.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("🧠 **Architect is thinking...**")
            
            try:
                # 🛠️ FIX FOR GROQ JSON ERROR: Use simple string for content
                if not st.session_state.agent_history:
                    agent_input = prompt
                else:
                    # Append new user message as a SIMPLE STRING to history
                    # This avoids nested JSON issues with Groq
                    agent_input = st.session_state.agent_history + [{"role": "user", "content": prompt}]
                
                async def get_response():
                    result = await run_study_agent(agent_input, model=model)
                    return result

                try:
                    loop = asyncio.get_running_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                
                result = asyncio.run(get_response())
                
                # Update history using to_input_list() which is standard SDK
                st.session_state.agent_history = result.to_input_list()
                
                response = result.final_output
                message_placeholder.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                st.rerun() 
            except Exception as e:
                message_placeholder.markdown(f"❌ **System Error:** {str(e)}")

# --- Notes Management ---
with st.expander("📂 Knowledge Base & File Management"):
    st.info("Upload your textbooks or study notes (.txt) here. The architect will use them for Doubt Solving.")
    uploaded_file = st.file_uploader("Upload Study Material", type=["txt"])
    if uploaded_file is not None:
        if not os.path.exists(NOTES_DIR):
            os.makedirs(NOTES_DIR)
        with open(os.path.join(NOTES_DIR, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Successfully integrated '{uploaded_file.name}' into my knowledge base!")
