import re
from openai import OpenAI

def mock_database_tool(order_number):
    """A mock tool for the ReAct pattern."""
    db = {
        "ORD123": "Shipped - arriving tomorrow.",
        "ORD999": "Delayed in transit due to weather.",
    }
    return db.get(order_number.upper(), "Order not found in system.")

def run_cot_bot(user_msg, api_key, model="llama-3.1-8b-instant", base_url="https://api.groq.com/openai/v1"):
    """
    Pattern 1: Chain of Thought
    Forces the bot to analyze sentiment and intent first.
    """
    system_prompt = """
    You are a premium customer support agent.
    You must structure your response strictly as follows:
    
    [INTERNAL THOUGHT]
    Sentiment: <analyze the customer's mood>
    Core Issue: <what do they actually want>
    Strategy: <how to reply effectively and empathetically>
    [/INTERNAL THOUGHT]
    
    [REPLY]
    <your actual message to the customer>
    [/REPLY]
    """
    
    client = OpenAI(api_key=api_key, base_url=base_url)
    res = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg}
        ]
    )
    return res.choices[0].message.content

def run_react_bot(user_msg, api_key, model="llama-3.1-8b-instant", base_url="https://api.groq.com/openai/v1"):
    """
    Pattern 2: ReAct (Reasoning + Acting)
    Gives the bot access to the database tool.
    """
    system_prompt = """
    You are a support bot. Your job is to check order statuses.
    If the user provides an order number, use the following format:
    
    Thought: The user wants to check an order.
    Action: check_order_status
    Action Input: <the order number>
    
    If you already know the status or don't need a tool, just answer normally with "Final Answer: "
    """
    
    client = OpenAI(api_key=api_key, base_url=base_url)
    res = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg}
        ],
        stop=["Observation:"]
    )
    
    msg = res.choices[0].message.content
    
    # Simple parse for ReAct
    if "Action: check_order_status" in msg:
        match = re.search(r"Action Input:\s*(\w+)", msg)
        if match:
            order_id = match.group(1)
            observation = mock_database_tool(order_id)
            return f"{msg}\n\n[SYSTEM TOOL EXECUTED]\nObservation: {observation}\n\n-> (The agent would now formulate a final answer based on this data)."
    
    return msg

def run_reflection_bot(user_msg, api_key, model="llama-3.1-8b-instant", base_url="https://api.groq.com/openai/v1"):
    """
    Pattern 3: Reflection
    Drafts a reply, then reviews it for tone.
    """
    client = OpenAI(api_key=api_key, base_url=base_url)
    
    # Step 1: Draft
    draft = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a busy, highly-efficient support worker. Write a quick, direct draft reply."},
            {"role": "user", "content": user_msg}
        ]
    ).choices[0].message.content
    
    # Step 2: Reflect and rewrite
    reflection_prompt = f"""
    You are the Quality Assurance Director for customer support.
    Below is a draft reply written by a junior agent. It might be too blunt or lack empathy.
    
    Customer said: "{user_msg}"
    Junior Draft: "{draft}"
    
    Review the draft. Explain what's wrong with it, and then provide a completely rewritten, highly empathetic version.
    """
    
    final = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": reflection_prompt}]
    ).choices[0].message.content
    
    return f"**[Step 1: Raw Draft]**\n{draft}\n\n---\n\n**[Step 2: QA Reflection & Final Rewrite]**\n{final}"
