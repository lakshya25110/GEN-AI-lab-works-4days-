import os
from openai import AsyncOpenAI
from agents import Agent, Runner, set_default_openai_client, function_tool

# Try to find the correct session import
try:
    from agents.memory import OpenAIConversationsSession as Session
except ImportError:
    try:
        from agents.sessions import InMemorySession as Session
    except ImportError:
        Session = None

def setup_agents_client(api_key: str, provider: str = "Groq"):
    """Configures the global OpenAI client. Provider: 'Groq' or 'OpenAI'."""
    if provider == "Groq":
        base_url = "https://api.groq.com/openai/v1"
    else:
        base_url = "https://api.openai.com/v1"
        
    client = AsyncOpenAI(api_key=api_key, base_url=base_url)
    set_default_openai_client(client)

def create_session():
    """Creates a new session for the agent if supported."""
    if Session:
        return Session()
    return None

from tools import get_local_notes, web_search, update_progress, get_progress

# --- Agent Definitions ---

def create_agents(model: str):
    planner_agent = Agent(
        name="Planner Agent",
        model=model,
        instructions="""You are a Senior Academic Architect specialized in study planning.
        Your style is professional, encouraging, and highly structured. 
        Use emojis 📅, 🚀, and 🎯 to make the interaction lively.
        
        Your Goal: Create personalized, time-bound study plans.
        - Use 'update_progress' to save topics to the user's plan.
        - Use 'get_progress' to check what's already planned.
        - Always provide a clear breakdown of topics, estimated time, and learning goals.""",
        tools=[update_progress, get_progress]
    )

    doubt_solver_agent = Agent(
        name="Doubt Solver Agent",
        model=model,
        instructions="""You are a Lively Senior Tutor and AI Architect.
        Your tone is engaging, inquisitive, and brilliant! Use emojis 💡, 📝, and 🔍.
        
        CRITICAL: If the user asks about ANY file, note, context, or data they've provided, 
        YOU MUST IMMEDIATELY use the 'get_local_notes' tool first.
        
        Logic:
        1. Check 'get_local_notes' for any file content.
        2. If not found or more info is needed, use 'web_search'.
        3. Explain the answer simply but deeply.
        
        If a user mentions they are done with a topic, use 'update_progress' to celebrate!""",
        tools=[get_local_notes, web_search, update_progress, get_progress]
    )

    triage_agent = Agent(
        name="Triage Agent",
        model=model,
        instructions="""You are the Lead AI Systems Architect and Concierge of this Study Assistant.
        Your job is to greet the user warmly and route them to the expert they need.
        
        LIVELY PERSONA: Use emojis like 👋, 🏦, and 🛠️.
        
        ROUTING RULES:
        - If the user asks about their files, notes, or uploaded documents, TRANSFER IMMEDIATELY to 'Doubt Solver Agent'.
        - If the user has a doubt or question, TRANSFER to 'Doubt Solver Agent'.
        - If the user wants a study plan or schedule, TRANSFER to 'Planner Agent'.
        - If they just want to see progress, use 'get_progress' yourself.
        
        ALWAYS initiate a handoff if the request is specific. Don't just stay in control.""",
        handoffs=[planner_agent, doubt_solver_agent],
        tools=[get_progress]
    )
    return triage_agent

async def run_study_agent(user_input, model: str):
    """
    Runs the triage agent loop.
    user_input can be a string (first turn) or a list of conversation items (history).
    """
    triage_agent = create_agents(model)
    result = await Runner.run(triage_agent, user_input)
    return result
