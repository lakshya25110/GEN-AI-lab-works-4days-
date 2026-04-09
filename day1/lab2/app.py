import streamlit as st
from cot_math import solve_math_problem, parse_cot_output

st.set_page_config(page_title="CoT Math Solver", page_icon="🧮")

st.title("🧮 CoT Math Solver Lab")
st.markdown("A demonstration of **Chain of Thought (CoT)** prompting for solving complex mathematical word problems.")

with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
    
    st.markdown("---")
    st.markdown("""
    **Sample Math Problems to Try:**
    - "A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost?"
    - "If it takes 5 machines 5 minutes to make 5 widgets, how long would it take 100 machines to make 100 widgets?"
    - "I have a 10 liter jug and a 3 liter jug. I need exactly 4 liters of water. How do I do it step by step?"
    """)

# Initialize session state for messages if we want a chat interface, 
# or just a simple form. Let's do a simple interactive form for this lab.

st.markdown("### Enter a Math Problem")
problem = st.text_area("Problem description:", height=100, placeholder="Type a tricky math word problem here...")

if st.button("Solve Problem 🚀"):
    if not api_key:
        st.error("Please enter your Groq API Key in the sidebar first!")
    elif not problem.strip():
        st.warning("Please enter a math problem.")
    else:
        with st.spinner("Thinking step-by-step..."):
            # Call the backend function
            raw_response = solve_math_problem(problem, api_key)
            
            if raw_response.startswith("Error:"):
                st.error(raw_response)
            else:
                # Parse the output
                parsed = parse_cot_output(raw_response)
                
                # Display the results beautifully
                st.subheader("Final Answer")
                st.success(f"**{parsed['final_answer']}**")
                
                st.subheader("How the AI thought about it (Chain of Thought)")
                with st.expander("View Reasoning Steps", expanded=True):
                    st.write(parsed["reasoning"])
                    
                with st.expander("View Raw LLM Output"):
                    st.code(parsed["raw"], language="text")
