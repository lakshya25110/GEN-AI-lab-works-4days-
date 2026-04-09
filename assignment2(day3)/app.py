import streamlit as st
import pandas as pd
from workflow import create_workflow

# UI Configuration
st.set_page_config(page_title="LangGraph Debugging Lab", layout="wide")

# Theme & Aesthetics
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
    }
    .bug-box {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #f44336;
        margin-bottom: 10px;
    }
    .fix-box {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ LangGraph Debugging Specialist Lab")
st.subheader("Analyze, Debug, and Fix Multi-Agent Workflows")

# State the 3 Intentional Bugs
with st.expander("🔍 View the 3 Intentional Bugs", expanded=False):
    st.markdown("""
    1. **Bug 1: State Overwrite** - The `messages` list in `state.py` is defined as a standard `list`. In LangGraph, without a reducer, the state is overwritten.
    2. **Bug 2: Routing Mismatch** - The `triage_node` returns capitalized strings like 'Billing', but the graph edges are configured for lowercase 'billing'.
    3. **Bug 3: Schema Violation** - The `support_node` returns an extra key `unrecognized_field` not defined in the `AgentState` TypedDict.
    """)

# Sidebar settings
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Groq API Key", value="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", type="password")
    mode = st.radio("Workflow Mode", options=["broken", "fixed"], format_func=lambda x: x.upper())
    st.info(f"Currently simulating: **{mode.upper()}** code.")

# Main Interface
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📥 Input Query")
    query = st.text_input("Enter a query (e.g., 'What is my billing status?')", "Why was I charged twice?")
    run_btn = st.button("🚀 Run Workflow")

if run_btn:
    if not api_key:
        st.error("Please provide a Groq API Key.")
    else:
        with st.spinner("Processing through LangGraph..."):
            try:
                # Initialize Workflow
                app = create_workflow(api_key, mode)
                
                # Initial State
                initial_state = {
                    "query": query,
                    "messages": ["User: " + query],
                    "execution_logs": ["Workflow started."]
                }
                
                # Execute
                result = app.invoke(initial_state)
                
                st.success("✅ Execution Complete")
                
                st.markdown("### 📝 Detailed Output")
                st.write("**Final Response:**", result.get("response", "N/A"))
                st.write("**Identified Category:**", result.get("category", "N/A"))
                
                st.markdown("### 🕒 Message History (State)")
                # If Bug 1 is present, this list will only show the LAST message
                for msg in result.get("messages", []):
                    st.info(msg)
                
                if len(result.get("messages", [])) < 2 and mode == "broken":
                    st.warning("⚠️ **State Loss Detected!** History was overwritten due to missing reducer.")

            except Exception as e:
                st.error(f"❌ Workflow Crashed: {str(e)}")
                if "KeyError" in str(e) or "routing" in str(e).lower():
                    st.markdown("""
                    <div class="bug-box">
                        <b>DIAGNOSIS:</b> Routing Error (Bug 2).<br>
                        The graph is trying to route to a capitalized node name that doesn't exist in the mapping.
                    </div>
                    """, unsafe_allow_html=True)

with col2:
    st.markdown("### 🕵️ Diagnostic Logs")
    if run_btn:
        st.json(result)
        
        st.markdown("### 🛠️ Explanations & Fixes")
        if mode == "broken":
            st.error("Bugs Detected in current run!")
            st.markdown("""
            - **Bug 1**: `messages` key is missing `Annotated[list, operator.add]`. Result: Only the last agent's message survived.
            - **Bug 2**: Triage returned 'Billing'. Route failed because mapping only knows 'billing'.
            - **Bug 3**: Returned `unrecognized_field`. This is bad practice and can cause runtime issues in strict environments.
            """)
        else:
            st.balloons()
            st.markdown("""
            <div class="fix-box">
                <b>FIXED LOGIC:</b><br>
                1. Added <code>Annotated[list, operator.add]</code> to State.<br>
                2. Standardized category strings to lowercase.<br>
                3. Sanitized node returns to match schema.
            </div>
            """, unsafe_allow_html=True)
