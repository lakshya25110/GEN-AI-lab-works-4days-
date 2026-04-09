import streamlit as st
import streamlit.components.v1 as components
import os
from pypdf import PdfReader
from workflow import create_workflow
from state import AgentState

# Page configuration
st.set_page_config(page_title="Agentic Recruitment Pipeline", layout="wide", page_icon="👔")

st.title("👔 Enterprise Recruitment Pipeline")
st.markdown("### Powered by LangGraph & Groq (Llama 3.1)")

# Sidebar for Configuration
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter Groq API Key", type="password", value="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")
    model = st.selectbox("Select Model", ["llama-3.1-70b-versatile", "llama-3.1-8b-instant"], index=0)
    
    st.divider()
    st.info("This system uses 3 specialized agents: Screening, Scheduling, and Evaluation.")

# Main Input Section
col1, col2 = st.columns([1, 1])

with col1:
    st.header("Candidate Resume")
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
    resume_text = ""
    if uploaded_file:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            resume_text += page.extract_text()
        st.success("Resume parsed successfully!")
        with st.expander("Show extracted text"):
            st.text(resume_text[:1000] + "...")

with col2:
    st.header("Job Description")
    jd = st.text_area("Paste Job Description here...", height=300, value="We are looking for a Python Developer with 3+ years of experience in Django, FastAPI, and LangChain. Should have experience with multi-agent systems and SQL databases.")

# Pipeline Execution
if st.button("🚀 Start Recruitment Pipeline", use_container_width=True):
    if not api_key:
        st.error("Please provide a Groq API Key.")
    elif not resume_text or not jd:
        st.error("Please provide both a resume and a job description.")
    else:
        with st.status("Initializing AI Agents...", expanded=True) as status:
            # 1. Setup Data
            initial_state = {
                "resume_text": resume_text,
                "job_description": jd,
                "candidate_info": None,
                "screening_score": None,
                "is_shortlisted": False,
                "interview_scheduled": False,
                "interview_slot": None,
                "interview_feedback": None,
                "final_score": None,
                "hiring_recommendation": None,
                "current_node": "START",
                "error": None
            }
            
            # 2. Compile Graph
            status.update(label="Compiling LangGraph workflow...", state="running")
            app = create_workflow(api_key, model)
            
            # 3. Stream Events
            status.update(label="Executing Pipeline...", state="running")
            placeholder = st.empty()
            
            for event in app.stream(initial_state):
                for node_name, state_update in event.items():
                    st.write(f"✅ Node Finished: **{node_name}**")
                    # Update local state display if needed
            
            # 4. Get Final Result
            final_result = app.invoke(initial_state)
            status.update(label="Pipeline Complete!", state="complete")

        # Display Results
        st.divider()
        st.header("📋 Pipeline Report")
        
        if final_result.get("error"):
            st.error(final_result["error"])
        else:
            res_col1, res_col2, res_col3 = st.columns(3)
            
            with res_col1:
                st.subheader("1. Screening")
                info = final_result.get("candidate_info")
                if info:
                    st.write(f"**Name:** {info.name}")
                    st.write(f"**Score:** {final_result.get('screening_score')}/100")
                    st.write(f"**Experience:** {info.experience_years} years")
                    st.write(f"**Shortlisted:** {'✅ Yes' if final_result.get('is_shortlisted') else '❌ No'}")
            
            with res_col2:
                st.subheader("2. Interview")
                if final_result.get("interview_scheduled"):
                    slot = final_result.get("interview_slot")
                    st.write(f"**Status:** Scheduled")
                    st.write(f"**Date:** {slot['date']}")
                    st.write(f"**Time:** {slot['time']}")
                else:
                    st.write("Status: Not Scheduled")
            
            with res_col3:
                st.subheader("3. Final Decision")
                st.metric("Final Score", f"{final_result.get('final_score') or 0}/100")
                rec = final_result.get("hiring_recommendation")
                if rec == "Strong Hire": st.success(rec)
                elif rec == "Hire": st.info(rec)
                elif rec == "Waitlist": st.warning(rec)
                else: st.error(rec or "Rejected")
# Display Results
        st.divider()

def st_mermaid(code: str):
    components.html(
        f"""
        <pre class="mermaid">
            {code}
        </pre>
        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true }});
        </script>
        """,
        height=600,
    )

# Workflow Visualization Section
st.divider()
st.subheader("🗺️ Workflow Diagram (LangGraph)")
st_mermaid("""
graph TD
    START((START)) --> Screen[Resume Screening Agent]
    Screen -->|Rejected| END((END))
    Screen -->|Shortlisted| Schedule[Interview Scheduling Agent]
    Schedule --> Eval[Candidate Evaluation Agent]
    Eval --> END
""")
