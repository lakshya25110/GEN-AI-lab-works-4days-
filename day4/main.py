import os
from dotenv import load_dotenv
from crewai import Crew, Process
from agents_config import get_agents
from tasks_config import get_tasks

# Load environment variables
load_dotenv()

def run_blog_crew(topic: str, audience: str = "Professional", tone: str = "Informative", model_name: str = "gpt-4o"):
    """Setup and kickoff the CrewAI blog generation team."""
    
    # 1. Initialize Agents
    researcher, writer, editor = get_agents(topic, model_name=model_name)
    
    # 2. Initialize Tasks
    tasks = get_tasks(researcher, writer, editor, topic)
    
    # 3. Instantiate the Crew
    blog_crew = Crew(
        agents=[researcher, writer, editor],
        tasks=tasks,
        process=Process.sequential, 
        verbose=True
    )
    
    # 4. Kickoff the process
    result = blog_crew.kickoff(inputs={
        'topic': topic,
        'audience': audience,
        'tone': tone
    })
    
    # Return the raw markdown string
    return result.raw if hasattr(result, 'raw') else str(result)

def save_to_markdown(content: str, topic: str):
    """Save the final result string to a markdown file."""
    filename = f"blog_{topic.lower().replace(' ', '_')}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return filename

if __name__ == "__main__":
    # Fallback to console if run directly
    user_topic = input("Enter the blog topic: ")
    if user_topic:
        final_result = run_blog_crew(user_topic)
        save_to_markdown(final_result, user_topic)
        print("\n✅ Done! Check the markdown file.")
