import os
import json
from typing import List, Dict, Any, Optional
from tavily import TavilyClient
from agents import function_tool

# File paths
STATE_FILE = "progress.json"
NOTES_DIR = "notes"

# Initialize Tavily
tavily_api_key = os.environ.get("TAVILY_API_KEY")
tavily = TavilyClient(api_key=tavily_api_key) if tavily_api_key else None

@function_tool
def get_local_notes(query: str) -> str:
    """
    Search through local text files for information related to the query.
    
    Args:
        query: The search term to look for in local notes.
    """
    results = []
    if not os.path.exists(NOTES_DIR):
        os.makedirs(NOTES_DIR)
        
    for filename in os.listdir(NOTES_DIR):
        if filename.endswith(".txt"):
            try:
                with open(os.path.join(NOTES_DIR, filename), "r", encoding="utf-8") as f:
                    content = f.read()
                    if query.lower() in content.lower():
                        results.append(f"--- From {filename} ---\n{content}")
            except Exception as e:
                continue
    
    if not results:
        return "No relevant notes found in local storage."
    return "\n\n".join(results)

@function_tool
def web_search(query: str) -> str:
    """
    Search the web for academic doubts or information. Use this if local notes are insufficient.
    
    Args:
        query: The academic question or topic to search for.
    """
    # Try to refresh client if key was added after import
    global tavily
    if not tavily:
        t_key = os.environ.get("TAVILY_API_KEY")
        if t_key:
            tavily = TavilyClient(api_key=t_key)
            
    if not tavily:
        return "Tavily API key not configured. Web search unavailable."
    
    try:
        search_result = tavily.search(query=query, search_depth="advanced")
        formatted_results = []
        for r in search_result.get('results', []):
            formatted_results.append(f"Source: {r['url']}\nContent: {r['content']}")
        return "\n\n".join(formatted_results)
    except Exception as e:
        return f"Error during web search: {str(e)}"

@function_tool
def update_progress(topic: str, status: str, timeframe: str = "") -> str:
    """
    Update the study plan progress. Use this to mark topics as 'Completed' or 'In Progress'.
    
    Args:
        topic: The name of the study topic.
        status: The current status ('Completed', 'In Progress', or 'Not Started').
        timeframe: Optional deadline or duration for the topic.
    """
    data = get_all_progress_data()
    
    found = False
    for item in data.get("topics", []):
        if item["name"].lower() == topic.lower():
            item["status"] = status
            if timeframe:
                item["timeframe"] = timeframe
            found = True
            break
            
    if not found:
        if "topics" not in data:
            data["topics"] = []
        data["topics"].append({
            "name": topic,
            "status": status,
            "timeframe": timeframe
        })
        
    with open(STATE_FILE, "w") as f:
        json.dump(data, f, indent=4)
        
    return f"Successfully updated progress for '{topic}' to '{status}'."

@function_tool
def get_progress() -> str:
    """
    Retrieve the current study plan and list of topics with their progress status.
    """
    data = get_all_progress_data()
    if not data or not data.get("topics"):
        return "No study plan found. User needs to generate one first."
    
    output = "Current Study Progress:\n"
    for item in data["topics"]:
        output += f"- {item['name']}: {item['status']} ({item.get('timeframe', 'No deadline')})\n"
    return output

def get_all_progress_data() -> Dict[str, Any]:
    """Helper to read the entire progress JSON."""
    if not os.path.exists(STATE_FILE):
        return {"topics": []}
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except:
        return {"topics": []}
