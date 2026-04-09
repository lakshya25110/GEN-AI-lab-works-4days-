from langgraph.graph import StateGraph, END
from state import AgentState
from agents import RecruitmentAgents

def create_workflow(api_key: str, model: str):
    # Initialize agents
    agents = RecruitmentAgents(api_key, model)
    
    # Initialize the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("screen_resume", agents.screen_resume)
    workflow.add_node("schedule_interview", agents.schedule_interview)
    workflow.add_node("evaluate_candidate", agents.evaluate_candidate)
    
    # Add entry point
    workflow.set_entry_point("screen_resume")
    
    # Define conditional edges
    def should_continue_to_interview(state: AgentState):
        if state.get("is_shortlisted"):
            return "schedule_interview"
        return END

    workflow.add_conditional_edges(
        "screen_resume",
        should_continue_to_interview,
        {
            "schedule_interview": "schedule_interview",
            "END": END
        }
    )
    
    # Define linear edges
    workflow.add_edge("schedule_interview", "evaluate_candidate")
    workflow.add_edge("evaluate_candidate", END)
    
    # Compile the graph
    return workflow.compile()
