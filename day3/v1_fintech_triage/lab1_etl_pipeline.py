"""
Lab 1: Fraud Detection ETL Pipeline using LangGraph
Extract -> Transform (Flag Suspicious) -> Load
"""

from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END

# 1. Define the State
class ETLState(TypedDict):
    raw_transactions: List[dict]
    processed_transactions: List[dict]
    load_status: str
    error: str

# 2. Define the Nodes
def extract_node(state: ETLState) -> ETLState:
    print("[Extract Node] Fetching banking transactions...")
    # Simulate API extraction from payment gateway
    data = [
        {"txn_id": "T001", "user": "Alice", "amount": 45.00, "location": "NY"},
        {"txn_id": "T002", "user": "Bob", "amount": 1500.00, "location": "Unknown"},
        {"txn_id": "T003", "user": "Charlie", "amount": 12.50, "location": "CA"}
    ]
    return {"raw_transactions": data}

def transform_node(state: ETLState) -> ETLState:
    print("[Transform Node] Running Fraud Detection logic...")
    raw_data = state.get("raw_transactions", [])
    
    if not raw_data:
        return {"error": "No transactions to process"}
        
    processed = []
    for txn in raw_data:
        # Business Logic: Transactions over $1000 or unknown locations are suspicious
        new_txn = txn.copy()
        is_high_value = txn["amount"] > 1000
        is_risky_loc = (txn["location"] == "Unknown")
        
        new_txn["is_suspicious"] = is_high_value or is_risky_loc
        processed.append(new_txn)
    
    return {"processed_transactions": processed}

def load_node(state: ETLState) -> ETLState:
    print("[Load Node] Loading suspicious records into Fraud DB...")
    data = state.get("processed_transactions", [])
    
    if not data:
        return {"load_status": "Failed: No data available", "error": state.get("error")}
        
    # Simulate loading data
    fraud_flags = sum(1 for txn in data if txn.get("is_suspicious"))
    summary = f"Processed {len(data)} transactions. Flagged {fraud_flags} as SUSPICIOUS."
    return {"load_status": summary}

# 3. Build the Graph
print("Building the Fraud ETL Graph...")
workflow = StateGraph(ETLState)

workflow.add_node("extract", extract_node)
workflow.add_node("transform", transform_node)
workflow.add_node("load", load_node)

workflow.add_edge(START, "extract")
workflow.add_edge("extract", "transform")
workflow.add_edge("transform", "load")
workflow.add_edge("load", END)

# Compile into an executable app
app = workflow.compile()

# 4. Execute the Graph
if __name__ == "__main__":
    print("\n--- Starting Fraud ETL Workflow ---")
    
    result = app.invoke({})
    
    print("\n--- Final Status ---")
    print(result.get("load_status"))
    if "processed_transactions" in result:
        print("\nProcessed Data Preview:")
        for r in result["processed_transactions"]:
            print(f"Txn: {r['txn_id']} | Amount: ${r['amount']} | Suspicious: {r['is_suspicious']}")
