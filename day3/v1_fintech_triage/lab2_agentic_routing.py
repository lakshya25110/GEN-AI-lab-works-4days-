"""
Lab 2: FinTech Customer Triage & Agentic Routing
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

# 1. Define the State
class AgentState(TypedDict):
    query: str
    category: str
    response: str
    requires_human: bool

# 2. Define the Nodes
def classifier_node(state: AgentState) -> dict:
    print(f"-> Analyzing customer query: '{state['query']}'")
    query = state["query"].lower()
    
    # NLP-style Intent Classification
    if "charge" in query or "fee" in query or "balance" in query:
        return {"category": "billing", "requires_human": False}
    elif "fraud" in query or "stolen" in query or "hacked" in query:
        return {"category": "investigation", "requires_human": False}
    else:
        return {"category": "unknown", "requires_human": True}

def billing_agent_node(state: AgentState) -> dict:
    print("-> Billing Agent: Fetching ledger data...")
    return {"response": "Billing Agent: I have reviewed your account regarding the charge."}

def fraud_agent_node(state: AgentState) -> dict:
    print("-> Fraud Agent: Freezing accounts and running security audit...")
    return {"response": "Fraud Agent: Warning! Security protocol initiated for hacked account."}

def human_review_node(state: AgentState) -> dict:
    print("-> High-Risk / Unknown Query! Escalating to Human Operator.")
    return {"response": "System Paused. A human operator will take over this thread."}

# 3. Define the Router Logic
def route_task(state: AgentState) -> str:
    if state.get("requires_human"):
        return "human_review"
    return state.get("category")

# 4. Build the Graph
workflow = StateGraph(AgentState)

workflow.add_node("classifier", classifier_node)
workflow.add_node("billing", billing_agent_node)
workflow.add_node("investigation", fraud_agent_node)
workflow.add_node("human_review", human_review_node)

workflow.add_edge(START, "classifier")

# Conditional edges dynamically route the query
workflow.add_conditional_edges(
    "classifier",
    route_task,
    {
        "billing": "billing",
        "investigation": "investigation",
        "human_review": "human_review"
    }
)

workflow.add_edge("billing", END)
workflow.add_edge("investigation", END)
workflow.add_edge("human_review", END)

# Checkpointing (Memory)
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

# 5. Execute Scenarios
if __name__ == "__main__":
    print("\n--- Scenario 1: Billing Issue ---")
    config1 = {"configurable": {"thread_id": "customer_101"}}
    res1 = app.invoke({"query": "Why was I charged a $15 late fee?"}, config1)
    print(res1.get("response"))
    
    print("\n--- Scenario 2: Emergency Escalation ---")
    config2 = {"configurable": {"thread_id": "customer_102"}}
    res2 = app.invoke({"query": "I want to speak to the CEO right now! Cancel my accounts!"}, config2)
    print(res2.get("response"))

    print("\n--- Checking Memory for Customer 102 ---")
    saved_state = app.get_state(config2).values
    print(f"Memory Checkpoint: Category={saved_state.get('category')} | Human={saved_state.get('requires_human')}")
