from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

class ModerationState(TypedDict):
    post_id: str
    content: str
    is_flagged: bool
    human_decision: str  # "approve" or "reject"
    final_status: str

def scan_node(state: ModerationState):
    content = state["content"].lower()
    # Simple flagged words simulation
    flagged = any(w in content for w in ["scam", "spam", "crypto", "hack", "buy"])
    return {"is_flagged": flagged}

def human_review_node(state: ModerationState):
    # Placeholder node. It doesn't modify anything, it's just the exact spot where execution PAUSES.
    pass

def publish_node(state: ModerationState):
    return {"final_status": "Published Successfully"}

def reject_node(state: ModerationState):
    return {"final_status": "Removed by Moderator"}

def route_after_scan(state: ModerationState):
    if state["is_flagged"]:
        return "human_review"
    return "publish_node"

def route_after_human(state: ModerationState):
    if state["human_decision"] == "approve":
        return "publish_node"
    return "reject_node"

workflow = StateGraph(ModerationState)
workflow.add_node("scan", scan_node)
workflow.add_node("human_review", human_review_node)
workflow.add_node("publish_node", publish_node)
workflow.add_node("reject_node", reject_node)

workflow.add_edge(START, "scan")
workflow.add_conditional_edges("scan", route_after_scan)
workflow.add_conditional_edges("human_review", route_after_human)
workflow.add_edge("publish_node", END)
workflow.add_edge("reject_node", END)

memory = MemorySaver()

# IMPORTANT: Setting `interrupt_before` means the graph pauses exactly BEFORE entering the Human phase.
app = workflow.compile(checkpointer=memory, interrupt_before=["human_review"])
