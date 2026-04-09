import streamlit as st
import os
import re
from openai import OpenAI

# ----------------- UI Config -----------------
st.set_page_config(page_title="ReAct Agent Lab", page_icon="🧠", layout="centered")

st.title("🧠 ReAct Agent Lab")
st.markdown("A demonstration of the Reasoning + Acting (ReAct) loop using OpenAI and a Mock Web Search tool.")

# Sidebar for API Key
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
    
    st.markdown("---")
    st.markdown("""
    **Mock Search Capabilities:**
    - "ceo of openai"
    - "sam altman age/born/birth year"
    - "capital of france"
    - "who won the world cup in 2022"
    """)

# ----------------- Agent Logic -----------------
SYSTEM_PROMPT = """
You are an intelligent reasoning agent designed to solve complex questions.
You work in a loop of Thought, Action, Action Input, and Observation.
At the end of your reasoning, you provide a Final Answer.

You have access to the following tools:
- Search: useful for searching the web for current facts, dates, or other information.

Use the following strict format for your responses:

Thought: <explain your reasoning step-by-step>
Action: <the tool to use, must be exactly "Search">
Action Input: <the query parameter for the tool>

(The system will provide an Observation based on your action)

When you have enough information to answer the user's question, use this format:
Thought: I now have the information I need.
Final Answer: <the complete answer to the original question>

Your goal is to be as accurate as possible. Only output ONE Action at a time.
"""

def search_tool(query):
    """Mock web search tool matching our lab setup."""
    query = query.lower()
    if "ceo of openai" in query:
        return "The CEO of OpenAI is Sam Altman."
    elif "sam altman" in query and ("age" in query or "birth" in query or "born" in query):
        return "Sam Altman was born on April 22, 1985."
    elif "capital of france" in query:
        return "The capital of France is Paris."
    elif "world cup" in query and "2022" in query:
        return "Argentina won the 2022 FIFA World Cup."
    else:
        return "Search results not found. Try a different variation of your query."

# ----------------- Chat UI -----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

user_query = st.chat_input("Ask a question (e.g. 'Who is the CEO of OpenAI and what is his birth year?')")

if user_query:
    if not api_key:
        st.error("Please enter your Groq API Key in the sidebar.")
        st.stop()
        
    client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
    
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)
    
    with st.chat_message("assistant"):
        st_status = st.status("Thinking...", expanded=True)
        
        agent_messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ]
        
        action_pattern = re.compile(r"Action:\s*(.*?)\nAction Input:\s*(.*)", re.IGNORECASE)
        final_answer_pattern = re.compile(r"Final Answer:\s*(.*)", re.IGNORECASE | re.DOTALL)
        
        max_steps = 5
        final_answer = None
        
        for step in range(max_steps):
            st_status.update(label=f"Step {step + 1}: Reasoning...", state="running")
            
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=agent_messages,
                    temperature=0.0,
                    stop=["Observation:"]
                )
            except Exception as e:
                error_msg = f"API Error: {str(e)}"
                st.error(error_msg)
                st_status.update(label="Error occurred", state="error")
                final_answer = "error" # Mark as not-None so we don't trigger the max steps block
                break
                
            ass_msg = response.choices[0].message.content
            agent_messages.append({"role": "assistant", "content": ass_msg})
            
            # Show the raw LLM output in the status box for learning purposes
            with st_status:
                st.markdown(f"**LLM Output:**\n```text\n{ass_msg}\n```")
            
            # Check for Final Answer
            final_match = final_answer_pattern.search(ass_msg)
            if final_match:
                final_answer = final_match.group(1).strip()
                st_status.update(label="Finished!", state="complete")
                st.write(f"**Final Answer:** {final_answer}")
                st.session_state.messages.append({"role": "assistant", "content": final_answer})
                break
                
            # Check for Action
            action_match = action_pattern.search(ass_msg)
            if action_match:
                action_name = action_match.group(1).strip()
                action_input = action_match.group(2).strip()
                
                with st_status:
                    if action_name == "Search":
                        st.info(f"🔍 Executing Tool: **{action_name}** with input: **'{action_input}'**")
                        observation = search_tool(action_input)
                    else:
                        st.error(f"⚠️ Unknown tool '{action_name}'")
                        observation = f"Error: Unknown tool '{action_name}'"
                        
                    st.success(f"👁️ Observation: {observation}")
                    st.markdown("---")
                
                agent_messages.append({"role": "user", "content": f"Observation: {observation}"})
            else:
                st.error("Error parsing LLM response")
                agent_messages.append({"role": "user", "content": "Error: You must provide a valid Action and Action Input or a Final Answer."})
                
        if not final_answer:
            st_status.update(label="Reached max reasoning steps.", state="error")
            st.error("The agent could not find the answer within the maximum allowed steps.")
