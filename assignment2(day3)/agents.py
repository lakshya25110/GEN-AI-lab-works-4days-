from langchain_groq import ChatGroq
from state import AgentState

class SpecialistAgents:
    def __init__(self, api_key: str):
        self.llm = ChatGroq(
            api_key=api_key,
            model_name="llama-3.1-8b-instant"
        )

    def triage_node(self, state: AgentState):
        """Categorizes the user query."""
        query = state["query"]
        prompt = f"Categorize this customer query into 'billing' or 'support'. Only return the word. Query: {query}"
        category = self.llm.invoke(prompt).content.strip().lower()
        
        # BUG 2 (Intentional): Returning 'Billing' (Capitalized) 
        # But the graph router will look for 'billing' (lowercase).
        # This causes conditional routing to fail or hit an END transition unexpectedly.
        buggy_category = "Billing" if "billing" in category else "Support"
        
        return {
            "category": buggy_category,
            "messages": [f"Triage: Classified as {buggy_category}"],
            "execution_logs": [f"Triage complete. Category: {buggy_category}"]
        }

    def billing_node(self, state: AgentState):
        """Handles billing queries."""
        return {
            "response": "Billing Agent: I have checked your invoices. No issues found.",
            "messages": ["Billing Agent: Handled billing."],
            "execution_logs": ["Billing Agent finished."]
        }

    def support_node(self, state: AgentState):
        """Handles general support queries."""
        
        # BUG 3 (Intentional): Returning a key 'unrecognized_field' not in AgentState.
        # This demonstrates a schema mismatch.
        return {
            "response": "Support Agent: I can help you with that general request.",
            "messages": ["Support Agent: Handled support."],
            "unrecognized_field": "This key does not exist in TypedDict",
            "execution_logs": ["Support Agent finished."]
        }
