import os
from crewai import Agent, LLM
from crewai_tools import SerperDevTool, TavilySearchTool

def get_agents(topic: str, model_name: str = "gpt-4o"):
    """Initialize and return the three specialized agents."""
    
    # 🛠️ NATIVE CREWAI LLM: This is the most robust way to handle multiple providers (OpenAI, Groq, etc.)
    # and avoid Pydantic validation errors.
    custom_llm = LLM(model=model_name)
    
    # Setup Search Tool 
    search_tool = None
    if os.environ.get("TAVILY_API_KEY"):
        search_tool = TavilySearchTool()
    elif os.environ.get("SERPER_API_KEY"):
        search_tool = SerperDevTool()

    # 🛠️ GROQ/LLAMA FIX: Disable delegation. 
    # Smaller models like Llama-3 sometimes struggle with complex tool delegation logic,
    # causing 'invalid_request_error'. In a sequential crew, delegation is rarely needed.

    # 1. Researcher
    researcher = Agent(
        role='Senior Research Analyst',
        goal=f'Conduct rigorous research on {topic} to uncover verified facts and breakthroughs.',
        backstory=(
            "You are a master of digital forensics. Your priority is FACTUAL ACCURACY. "
            "You cross-reference data from multiple sources. You DO NOT delegate work. "
            "You focus entirely on your task of gathering information."
        ),
        tools=[search_tool] if search_tool else [],
        llm=custom_llm,
        allow_delegation=False, # DISABLED for Groq stability
        verbose=True
    )

    # 2. Writer
    writer = Agent(
        role='Content Strategist & Professional Writer',
        goal=f'Craft a high-quality blog post about {topic} based EXCLUSIVELY on provided research.',
        backstory=(
            "You are a narrative expert who transforms dry facts into compelling stories. "
            "You do NOT make up facts. If information is missing from the research report, "
            "you highlight it rather than hallucinating. You focus entirely on writing."
        ),
        llm=custom_llm,
        allow_delegation=False, # DISABLED for Groq stability
        verbose=True
    )

    # 3. Editor
    editor = Agent(
        role='Chief Content Editor & Fact Checker',
        goal=f'Review the blog post for {topic} to ensure perfection and factual alignment.',
        backstory=(
            "You are the final line of defense. You compare the draft against the research report. "
            "You focus entirely on polishing and refining the content provided."
        ),
        llm=custom_llm,
        allow_delegation=False, # DISABLED for Groq stability
        verbose=True
    )

    return researcher, writer, editor
