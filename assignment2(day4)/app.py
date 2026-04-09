import os
import streamlit as st
from crewai import Agent, Task, Crew, Process
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_groq import ChatGroq

# Setup Streamlit page configuration
st.set_page_config(page_title="CrewAI Research Pipeline", page_icon="🔍", layout="wide")

st.title("🔍 Industry Research Multi-Agent Pipeline")
st.markdown("Use this UI to run a 3-agent CrewAI pipeline that fetches news, summarizes insights, and generates an executive report.")

# Sidebar for configuration
st.sidebar.title("Configuration")
st.sidebar.info("As requested, the Groq API key is pre-filled in the UI input rather than hardcoded globally.")
api_key = st.sidebar.text_input("Groq API Key", type="password", value="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")

topic = st.text_input("Enter the Industry Topic to Research:", value="AI industry")
run_button = st.button("Generate Report", type="primary")

if run_button:
    if not api_key:
        st.error("Please enter your Groq API Key in the sidebar.")
    else:
        # Set the API key dynamically based on UI input
        os.environ["GROQ_API_KEY"] = api_key
        
        try:
            # Initialize Groq LLM (llama3-8b-8192 is widely supported for fast reasoning)
            llm = ChatGroq(temperature=0.7, model_name="llama3-8b-8192")
        except Exception as e:
            st.error(f"Failed to initialize Groq LLM. Please check your API key or model name. Error: {e}")
            st.stop()
            
        with st.spinner("Initializing CrewAI Agents..."):
            search_tool = DuckDuckGoSearchRun()

            # --------------------------
            # 1. Agent Definitions
            # --------------------------
            researcher = Agent(
                role="Senior Industry Researcher",
                goal="Fetch the latest and most relevant news, breakthroughs, and data regarding the assigned industry topic.",
                backstory="You are an expert researcher with a keen eye for emerging trends. You navigate unstructured data to pinpoint what matters.",
                verbose=True,
                allow_delegation=False,
                tools=[search_tool],
                llm=llm
            )

            summarizer = Agent(
                role="Insight Summarizer",
                goal="Extract and condense key insights, emerging trends, and important data points from raw research.",
                backstory="You have a unique talent for distilling complex information into actionable core facts.",
                verbose=True,
                allow_delegation=False,
                llm=llm
            )

            report_generator = Agent(
                role="Executive Report Generator",
                goal="Compile a structured, professional executive report based on summarized insights.",
                backstory="You structure information clearly for executives, transforming bullets into compelling narratives.",
                verbose=True,
                allow_delegation=False,
                llm=llm
            )

            # --------------------------
            # 2. Task Definitions
            # --------------------------
            research_task = Task(
                description=f"Search the web for the latest trends in the '{topic}' industry. Focus on breakthroughs, market shifts, and major company announcements. Gather factual information.",
                expected_output=f"A compiled dossier of the latest news and facts regarding the '{topic}' industry.",
                agent=researcher
            )

            summarize_task = Task(
                description="Review the research dossier. Identify top 3-5 emerging trends. Condense the information into actionable insights and extract key data points.",
                expected_output="A concise brief highlighting major trends and data points.",
                agent=summarizer,
                context=[research_task]
            )

            report_task = Task(
                description="Use summarized insights to generate a final, professional executive report. Structure exactly with: 1. Executive Summary, 2. Detailed Trends Analysis, 3. Strategic Implications. Format it in clean Markdown.",
                expected_output=f"A structured Executive Report in Markdown format detailing trends in '{topic}'.",
                agent=report_generator,
                context=[summarize_task]
            )

            # --------------------------
            # 3. Crew Assembly & Execution
            # --------------------------
            research_crew = Crew(
                agents=[researcher, summarizer, report_generator],
                tasks=[research_task, summarize_task, report_task],
                process=Process.sequential,
                verbose=True
            )

        with st.status("Agents are actively researching and generating the report (this may take 1-2 minutes)...", expanded=True) as status:
            st.write("Agent 1: Searching the web for the latest facts...")
            st.write("Agent 2: Summarizing insights...")
            st.write("Agent 3: Compiling final report...")
            
            try:
                # Kickoff the pipeline
                result = research_crew.kickoff(inputs={'topic': topic})
                status.update(label="Report Generation Complete!", state="complete", expanded=False)
                
                # Display output
                st.markdown("---")
                st.markdown(f"## Final Executive Report: {topic.title()}")
                st.markdown(result.raw if hasattr(result, "raw") else result) # handle crewai 0.3x output format
            except Exception as e:
                status.update(label="An error occurred during workflow execution.", state="error")
                st.error(f"Execution Error: {e}")
