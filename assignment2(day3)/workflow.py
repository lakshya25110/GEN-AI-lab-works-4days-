import operator
from typing import TypedDict, Annotated, Literal
from langgraph.graph import StateGraph, START, END
from agents import SpecialistAgents
from state import AgentState

# --- FIXED STATE ---
class FixedAgentState(TypedDict):
    query: str
    category: str
    response: str
    # FIX for Bug 1: Use operator.add to accumulate messages
    messages: Annotated[list, operator.add]
    execution_logs: Annotated[list, operator.add]

# --- NODES FOR FIXED VERSION ---
def fixed_triage_node(state, agents):
    result = agents.triage_node(state)
    # FIX for Bug 2: Ensure lowercase category to match edge mapping
    result["category"] = result["category"].lower() 
    return result

def fixed_support_node(state, agents):
    result = agents.support_node(state)
    # FIX for Bug 3: Remove unrecognized fields
    if "unrecognized_field" in result:
        del result["unrecognized_field"]
    return result

def create_workflow(api_key: str, mode: Literal["broken", "fixed"]):
    agents = SpecialistAgents(api_key)
    
    # Select state schema
    StateClass = AgentState if mode == "broken" else FixedAgentState
    workflow = StateGraph(StateClass)
    
    # Add Nodes
    if mode == "broken":
        workflow.add_node("triage", agents.triage_node)
        workflow.add_node("billing", agents.billing_node)
        workflow.add_node("support", agents.support_node)
    else:
        # Use wrapper functions for fixed logic
        workflow.add_node("triage", lambda s: fixed_triage_node(s, agents))
        workflow.add_node("billing", agents.billing_node)
        workflow.add_node("support", lambda s: fixed_support_node(s, agents))

    # Entry Point
    workflow.add_edge(START, "triage")
    
    # Routing Logic
    def router(state):
        return state.get("category")

    # Conditional Edges
    # BUG 2 (Intentional): The mapping expects lowercase 'billing' and 'support'.
    # But inside agents.triage_node (broken mode), it returns 'Billing' or 'Support'.
    workflow.add_conditional_edges(
        "triage",
        router,
        {
            "billing": "billing",
            "support": "support",
            "unknown": END
        }
    )
    
    workflow.add_edge("billing", END)
    workflow.add_edge("support", END)
    
    return workflow.compile()
