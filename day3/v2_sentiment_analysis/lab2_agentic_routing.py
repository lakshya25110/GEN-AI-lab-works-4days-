"""
Lab 2: Conditional Branching for Dynamic Decisions (Sentiment Analysis)
"""

from typing import TypedDict
import urllib.request
import json
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

# 1. Define the State
class AgentState(TypedDict):
    query: str
    sentiment: str  # POSITIVE or NEGATIVE
    category: str
    response: str
    requires_human: bool

# --- Hugging Face Sentiment Model ---
def hf_sentiment_analysis(text: str) -> str:
    """Calls Hugging Face Inference API for distilbert sentiment analysis."""
    print(f"[HF Model] Analyzing sentiment for: '{text}'")
    url = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
    data = json.dumps({"inputs": text}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        # Result format: [[{'label': 'POSITIVE', 'score': 0.99}, ...]]
        label = result[0][0]['label']
        print(f"[HF Model] API Output -> {label}")
        return label
    except Exception as e:
        # Fallback Mock if Hugging Face API is rate-limited or offline
        print(f"[HF Model] API unavailable, using fallback heuristic. Error: {e}")
        text_lower = text.lower()
        if any(w in text_lower for w in ["angry", "bad", "terrible", "cancel", "sue", "hate", "lawyer"]):
            return "NEGATIVE"
        return "POSITIVE"

# 2. Define the Nodes
def classifier_node(state: AgentState) -> dict:
    query = state["query"]
    sentiment = hf_sentiment_analysis(query)
    
    # Conditional logic based on Sentiment
    if sentiment == "POSITIVE":
        return {"sentiment": sentiment, "category": "rewards", "requires_human": False}
    else:  # NEGATIVE
        # If the negative query contains legal threats, escalate
        if "sue" in query.lower() or "lawyer" in query.lower():
            return {"sentiment": sentiment, "category": "legal", "requires_human": True}
        else:
            return {"sentiment": sentiment, "category": "support", "requires_human": False}

def rewards_agent_node(state: AgentState) -> dict:
    print("-> Rewards Agent: Offering loyalty discounts...")
    return {"response": "Rewards Agent: We are so happy you love our service! Here is a 10% discount code."}

def support_agent_node(state: AgentState) -> dict:
    print("-> Support Agent: Initiating de-escalation protocol...")
    return {"response": "Support Agent: I apologize for the terrible experience. Let me fix that right now."}

def human_review_node(state: AgentState) -> dict:
    print("-> Extremely Negative / Legal Threat! Escalating to Human Manager.")
    return {"response": "System Paused. A human manager is reviewing this legal threat."}

# 3. Define the Router Logic
def route_task(state: AgentState) -> str:
    if state.get("requires_human"):
        return "human_review"
    return state.get("category")

# 4. Build the Graph
workflow = StateGraph(AgentState)

workflow.add_node("classifier", classifier_node)
workflow.add_node("rewards", rewards_agent_node)
workflow.add_node("support", support_agent_node)
workflow.add_node("human_review", human_review_node)

workflow.add_edge(START, "classifier")

# Conditional edges dynamically route the query
workflow.add_conditional_edges(
    "classifier",
    route_task,
    {
        "rewards": "rewards",
        "support": "support",
        "human_review": "human_review"
    }
)

workflow.add_edge("rewards", END)
workflow.add_edge("support", END)
workflow.add_edge("human_review", END)

# Checkpointing (Memory)
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

# 5. Execute Scenarios
if __name__ == "__main__":
    print("\n--- Scenario 1: Happy Customer ---")
    res1 = app.invoke({"query": "I absolutely love your new update, it works great!"}, {"configurable": {"thread_id": "1"}})
    print(res1.get("response"))
    
    print("\n--- Scenario 2: Angry Customer ---")
    res2 = app.invoke({"query": "This app is terrible and ruined my data. Fix it!"}, {"configurable": {"thread_id": "2"}})
    print(res2.get("response"))

    print("\n--- Scenario 3: Legal Escalation ---")
    res3 = app.invoke({"query": "I hate you, I am going to call my lawyer and sue you."}, {"configurable": {"thread_id": "3"}})
    print(res3.get("response"))
