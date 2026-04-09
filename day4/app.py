import streamlit as st
import os
from main import run_blog_crew, save_to_markdown

# --- UI Setup ---
st.set_page_config(page_title="Blog Crew: AI Editorial Team", page_icon="✍️", layout="wide")

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background: #FF4B4B !important;
        color: white !important;
        font-weight: bold;
    }
    .status-card {
        padding: 20px;
        border-radius: 10px;
        background: #1e2129;
        border-left: 5px solid #FF4B4B;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("✍️ Blog Generation Crew")
st.markdown("Collaborative AI Agents: Researcher → Writer → Editor")

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Configuration")
    topic = st.text_input("Blog Topic", placeholder="e.g. The Future of GenAI")
    audience = st.selectbox("Target Audience", ["Professional", "General Public", "Technical Experts", "Students"])
    tone = st.selectbox("Tone", ["Informative", "Persuasive", "Conversational", "Academic"])
    
    provider = st.radio("AI Provider", ["Groq", "OpenAI"], index=0)
    
    if provider == "Groq":
        model = st.selectbox("Model", ["groq/llama-3.3-70b-versatile", "groq/llama-3.1-405b-reasoning", "groq/llama-3.1-8b-instant"])
    else:
        model = st.selectbox("Model", ["gpt-4o", "gpt-4o-mini"])
    
    st.divider()
    st.info("The crew will research, draft, and polish your post sequentially.")

# --- Action ---
if st.button("🚀 Kickoff Editorial Team"):
    if not topic:
        st.error("Please enter a topic first!")
    else:
        with st.status("🛠️ Editorial Team at work...", expanded=True) as status:
            st.write(f"🔄 Initializing {provider} Agent with {model}...")
            try:
                # Run the crew
                final_content = run_blog_crew(topic, audience, tone, model_name=model)
                
                st.write("📝 Writer has completed the draft...")
                st.write("✨ Editor has polished the final copy...")
                
                status.update(label="✅ Blog Generation Complete!", state="complete", expanded=False)
                
                # Show results
                st.divider()
                st.subheader(f"📄 Final Result: {topic}")
                st.markdown(final_content)
                
                # Save and Download
                filename = save_to_markdown(final_content, topic)
                st.success(f"Saved locally as {filename}")
                
                st.download_button(
                    label="📥 Download Blog Post (.md)",
                    data=final_content,
                    file_name=filename,
                    mime="text/markdown"
                )
                
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                status.update(label="❌ Generation Failed", state="error")

# --- Footer ---
st.divider()
st.caption("Powered by CrewAI & Groq/OpenAI")
