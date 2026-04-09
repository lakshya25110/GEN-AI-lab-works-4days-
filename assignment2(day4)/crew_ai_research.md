# Industry Research Multi-Agent Pipeline

## 1. CrewAI Code

The following Python script defines a 3-agent CrewAI pipeline. It utilizes the `langchain-community` library for web search capabilities (via DuckDuckGo) to simulate an authentic research environment. 

```python
import os
from crewai import Agent, Task, Crew, Process
from langchain_community.tools import DuckDuckGoSearchRun

# Initialize the research tool for web searches
search_tool = DuckDuckGoSearchRun()

# --------------------------
# 1. Agent Definitions
# --------------------------

researcher = Agent(
    role="Senior Industry Researcher",
    goal="Fetch the latest and most relevant news, breakthroughs, and data regarding the assigned industry topic.",
    backstory=(
        "You are an expert researcher with a keen eye for emerging trends. "
        "You excel at navigating vast amounts of unstructured data on the web to "
        "pinpoint exactly what matters most for strategic decision-making. You never make things up."
    ),
    verbose=True,
    allow_delegation=False,
    tools=[search_tool]
)

summarizer = Agent(
    role="Insight Summarizer",
    goal="Extract and condense key insights, emerging trends, and important data points from raw research.",
    backstory=(
        "You have a unique talent for distilling complex, lengthy information. "
        "You read through extensive research data and extract the necessary core facts, "
        "highlighting the 'so what?' for business leaders. You remove noise and focus on signal."
    ),
    verbose=True,
    allow_delegation=False,
)

report_generator = Agent(
    role="Executive Report Generator",
    goal="Compile a structured, professional executive report based on summarized insights.",
    backstory=(
        "You are a seasoned business communicator and analyst. You know how to structure "
        "information so that it is instantly clear to executives. You transform raw bullet points "
        "into compelling, professionally formatted narratives."
    ),
    verbose=True,
    allow_delegation=False,
)

# --------------------------
# 2. Task Definitions
# --------------------------

research_task = Task(
    description=(
        "Search the web for the latest trends in the '{topic}' industry. "
        "Focus on technological breakthroughs, market shifts, and major company announcements from the last 6 months. "
        "Gather detailed, factual information and ensure diverse sources."
    ),
    expected_output="A compiled dossier of the latest news, facts, and events regarding the '{topic}' industry, including sources where possible.",
    agent=researcher
)

summarize_task = Task(
    description=(
        "Review the research dossier provided by the Researcher. "
        "Identify the top 3-5 emerging trends. Condense the information into actionable insights "
        "and extract specific data points, statistics, or major technological milestones."
    ),
    expected_output="A concise brief highlighting 3-5 major trends and key data points, stripped of fluff.",
    agent=summarizer,
    context=[research_task]  # Enforces sequence: Wait for research_task to finish
)

report_task = Task(
    description=(
        "Using the summarized insights, generate a final, professional executive report. "
        "Structure the report exactly with: 1. Executive Summary, 2. Detailed Trends Analysis, 3. Strategic Implications. "
        "Format it in clean Markdown, ensuring a highly professional and analytical tone."
    ),
    expected_output="A structured Executive Report in Markdown format detailing the trends in '{topic}'.",
    agent=report_generator,
    context=[summarize_task] # Enforces sequence: Wait for summarize_task to finish
)

# --------------------------
# 3. Crew Assembly & Execution
# --------------------------

research_crew = Crew(
    agents=[researcher, summarizer, report_generator],
    tasks=[research_task, summarize_task, report_task],
    process=Process.sequential, # Execute tasks strictly in order
    verbose=True
)

if __name__ == "__main__":
    # Define the domain dynamically
    industry_topic = "AI industry"
    
    # Kickoff the pipeline
    print(f"Starting research sequence for: {industry_topic}...\n")
    result = research_crew.kickoff(inputs={'topic': industry_topic})
    
    print("\n" + "="*50)
    print("FINAL REPORT GENERATED")
    print("="*50 + "\n")
    print(result)
```

---

## 2. Sample Report Output

*This represents the dynamic outcome produced by Agent 3 (Report Generator), utilizing the pipeline above.*

# Executive Research Report: State of the AI Industry

## 1. Executive Summary
The artificial intelligence industry is experiencing continuous, rapid acceleration marked by the wide availability of advanced multimodality, decreasing costs of inference, and expanding enterprise adoption. The shift has moved from demonstrating capability to optimizing efficiency and integrating into custom commercial workflows. This report outlines the most critical shifts in the AI landscape over recent months, serving as a tactical overview for executive stakeholders.

## 2. Detailed Trends Analysis

**Trend 1: The Rise of Multimodal and Agentic AI**
Current generation Large Language Models (LLMs) have actively expanded beyond text generation. Models like GPT-4o, Gemini 1.5 Pro, and Claude 3.5 Sonnet now natively process audio, vision, and large context windows seamlessly. Furthermore, AI systems are migrating from passive chatbots to "Agentic" workflows capable of multi-step planning, tool use, and autonomous problem-solving.
* *Key Insight:* Agentic frameworks like LangGraph and CrewAI are seeing mass developer adoption to bridge the gap between static LLMs and autonomous software systems.

**Trend 2: Commoditization of Open-Weight Models**
Open-weight models, championed predominantly by Meta (Llama 3 series) and Mistral AI, have closed the performance gap with proprietary frontier models.
* *Key Data Point:* Llama 3 70B performance reliably rivals closed-source models from previous quarters, forcing API providers to slash inference pricing.
* *Key Insight:* Enterprises are increasingly favoring fine-tuning open models to ensure data privacy and prevent vendor lock-in.

**Trend 3: Custom Silicon and Infrastructure Optimization**
The bottleneck in AI scalability remains compute hardware. While Nvidia continues to dominate the GPU landscape with its Hopper and upcoming Blackwell architectures, cloud providers (Google TPU, AWS Trainium, Microsoft Maia) and private silicon startups (Groq, Cerebras) are heavily optimizing for low-latency inference speeds.
* *Key Data Point:* Groq's LPU architecture is unlocking real-time inference speeds exceeding 800 tokens per second for specific open-weight models.

## 3. Strategic Implications
* **Security vs. Speed:** Organizations must carefully balance robust compliance with the rapid deployment of agentic pipelines. 
* **Compute Independence:** Developing infrastructure agnostic systems allows businesses to shift between cloud providers or local deployments as compute costs fluctuate.
* **Talent Reallocation:** The engineering focus is shifting from "Prompt Engineering" to "AI Architecture"—designing fault-tolerant, multi-agent networks that orchestrate business logic securely.
