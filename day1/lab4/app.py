import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from support_bot import run_cot_bot, run_react_bot, run_reflection_bot

st.set_page_config(page_title="Prompt Engineering Hub", page_icon="💡")

st.title("💡 Prompt Engineering Challenge")
st.markdown("Test out the three advanced prompt patterns (Chain of Thought, ReAct, Self-Reflection) within a Customer Support Chatbot context.")

with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
    
    st.markdown("---")
    st.markdown("""
    **Test Scenarios to Try:**
    - "My order ORD123 hasn't arrived. I'm leaving for vacation tomorrow and I am furious!"
    - "Where is ORD999? Explain it clearly."
    """)

tab1, tab2, tab3 = st.tabs(["🧩 1. Chain of Thought", "⚙️ 2. ReAct (Tools)", "🪞 3. Self-Reflection"])

# --- TAB 1: Chain of Thought ---
with tab1:
    st.markdown("### Pattern 1: CoT Sentiment Analysis")
    st.caption("Forces the bot to evaluate the user's emotional state before writing a response.")
    msg1 = st.text_area("Customer Message:", key="cot_msg")
    
    if st.button("Run CoT Bot", key="btn1"):
        if not api_key:
            st.error("API Key required.")
        else:
            with st.spinner("Analyzing..."):
                res = run_cot_bot(msg1, api_key)
                st.code(res, language="markdown")

# --- TAB 2: ReAct ---
with tab2:
    st.markdown("### Pattern 2: ReAct Order Lookup")
    st.caption("Gives the bot access to a mock backend database to check order statuses via the ReAct framework.")
    msg2 = st.text_area("Customer Message (Include ORD123 or ORD999):", key="react_msg")
    
    if st.button("Run ReAct Bot", key="btn2"):
        if not api_key:
            st.error("API Key required.")
        else:
            with st.spinner("Deciding on an action..."):
                res = run_react_bot(msg2, api_key)
                st.info(res)

# --- TAB 3: Reflection ---
with tab3:
    st.markdown("### Pattern 3: QA Self-Reflection")
    st.caption("A junior bot drafts a fast reply, and a senior QA bot reflects on it to improve tone and empathy.")
    msg3 = st.text_area("Customer Message:", key="reflect_msg")
    
    if st.button("Run Reflection Bot", key="btn3"):
        if not api_key:
            st.error("API Key required.")
        else:
            with st.spinner("Drafting and Verifying..."):
                res = run_reflection_bot(msg3, api_key)
                st.markdown(res)
