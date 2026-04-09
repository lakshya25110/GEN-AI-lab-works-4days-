import streamlit as st
from reviewer import self_reflecting_reviewer

st.set_page_config(page_title="Self-Reflecting Reviewer", page_icon="🤖")

st.title("🤖 Self-Reflecting Code Agent")
st.markdown("This AI acts as both a **Creator** and a **Verifier**. It generates Python code, runs an internal parsing check using the `ast` module, and automatically asks itself to fix any Syntax Errors it encounters before showing you the result.")

with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
    
    st.markdown("---")
    st.markdown("""
    **Intentional Bugs to Try:**
    ```python
    def calculate_total(prices)
        total = 0
        for p in prices
            total += p
        return total
    ```
    *(Watch the agent generate code, fail AST validation due to missing colons, and loop to fix it!)*
    """)

st.markdown("### Paste Broken Python Code")
user_code = st.text_area("Code for review:", height=200, placeholder="def hello_world()\n    print('Hello')")

if st.button("Start Reflection Loop 🧠"):
    if not api_key:
        st.error("Please enter your Groq API Key in the sidebar.")
    elif not user_code.strip():
        st.warning("Please enter some code to review.")
    else:
        st.markdown("### Agent Reflection Log")
        log_container = st.container()
        
        # We'll use this spinner to show action is ongoing
        with st.status("Initializing self-reflection...", expanded=True) as status_box:
            
            # Start the generator
            agent_iterator = self_reflecting_reviewer(user_code, api_key)
            
            final_code = None
            full_review = None
            
            for step_data in agent_iterator:
                # Handle status updates
                if step_data["type"] == "info":
                    st.info(f"🔄 {step_data['status']}")
                elif step_data["type"] == "warning":
                    st.warning(f"⚠️ {step_data['status']}")
                    if "extracted" in step_data:
                        st.code(step_data["extracted"], language="python")
                elif step_data["type"] == "error":
                    status_box.update(label="Process Failed", state="error")
                    st.error(f"❌ {step_data['status']}")
                elif step_data["type"] == "success":
                    status_box.update(label="Code Validated!", state="complete")
                    st.success(f"✅ {step_data['status']}")
                    final_code = step_data.get("final_code")
                    full_review = step_data.get("full_response")
                    
                # Did we finish?
                if step_data.get("done"):
                    break
        
        # Display the Final Result beautifully outside the status box
        if final_code:
            st.markdown("---")
            st.subheader("🎉 Final Validated Code")
            st.code(final_code, language="python")
            
            with st.expander("Read Full Code Review"):
                st.markdown(full_review)
