from typing import TypedDict, Annotated
import operator

# NOTE: In LangGraph, if multiple nodes return the same key, it OVERWRITES by default.
# To accumulate (e.g., chat history), we MUST use a reducer.

class AgentState(TypedDict):
    """
    Standard state schema for our Customer Support Agent.
    """
    query: str
    category: str
    response: str
    # BUG 1 (Intentional): This list will overwrite itself instead of appending history.
    # FIXED Version would be: messages: Annotated[list, operator.add] or add_messages
    messages: list 
    
    # We will use this to track errors for the UI
    execution_logs: Annotated[list, operator.add]
