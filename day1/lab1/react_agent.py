import os
import re
from openai import OpenAI

# Initialize the OpenAI client
# Ensure the OPENAI_API_KEY environment variable is set
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "your-api-key-here"))

# 1. Define the System Prompt
# Here we enforce the strict ReAct format: Thought -> Action -> Action Input
SYSTEM_PROMPT = """
You are an intelligent reasoning agent designed to solve complex questions.
You work in a loop of Thought, Action, Action Input, and Observation.
At the end of your reasoning, you provide a Final Answer.

You have access to the following tools:
- Search: useful for searching the web for current facts, dates, or other information.

Use the following strict format for your responses:

Thought: <explain your reasoning step-by-step>
Action: <the tool to use, must be exactly "Search">
Action Input: <the query parameter for the tool>

(The system will provide an Observation based on your action)

When you have enough information to answer the user's question, use this format:
Thought: I now have the information I need.
Final Answer: <the complete answer to the original question>

Your goal is to be as accurate as possible. Only output ONE Action at a time.
"""

# 2. Integrate a Web Search Function
def search_tool(query):
    """
    Mock web search tool. 
    In a real-world scenario, you would integrate a Serper API, DuckDuckGo, or Google Search.
    """
    print(f"  [Tool Executed] -> Searching for: '{query}'")
    
    # Simple hardcoded mock database for our lab examples
    query = query.lower()
    if "ceo of openai" in query:
        return "The CEO of OpenAI is Sam Altman."
    elif "sam altman age" in query or "birth year" in query or "born" in query:
        return "Sam Altman was born on April 22, 1985."
    elif "capital of france" in query:
        return "The capital of France is Paris."
    elif "who won the world cup in 2022" in query:
        return "Argentina won the 2022 FIFA World Cup."
    else:
        return "Search results not found. Try a different variation of your query."

# 3. Define the ReAct Agent Loop
def react_agent(question, max_steps=5):
    """
    Runs the ReAct reasoning loop until a Final Answer is reached or max_steps is hit.
    """
    print(f"\n--- Starting ReAct Agent ---")
    print(f"User Question: {question}\n")
    
    # Initialize messages list with the system prompt and the user's question
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question}
    ]
    
    # Regex patterns to parse out the Action and Final Answer
    action_pattern = re.compile(r"Action:\s*(.*?)\nAction Input:\s*(.*)", re.IGNORECASE)
    final_answer_pattern = re.compile(r"Final Answer:\s*(.*)", re.IGNORECASE | re.DOTALL)
    
    for step in range(max_steps):
        print(f"Step {step + 1}: Let me think...")
        
        # Call the OpenAI API
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo", # You can use gpt-4 for better reasoning
                messages=messages,
                temperature=0.0, # Zero temperature for deterministic reasoning
                stop=["Observation:"] # VERY IMPORTANT: Force LLM to stop generating before it hallucinates an observation
            )
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return "Failed to get response."
            
        ass_msg = response.choices[0].message.content
        print(f"\n[Agent output]:\n{ass_msg}\n")
        
        # Append the agent's thought/action to the messages history
        messages.append({"role": "assistant", "content": ass_msg})
        
        # Parse for a Final Answer
        final_match = final_answer_pattern.search(ass_msg)
        if final_match:
            final_answer = final_match.group(1).strip()
            print(f"\n>>> FINAL ANSWER: {final_answer}")
            return final_answer
            
        # Parse for an Action
        action_match = action_pattern.search(ass_msg)
        if action_match:
            action_name = action_match.group(1).strip()
            action_input = action_match.group(2).strip()
            
            if action_name == "Search":
                observation = search_tool(action_input)
            else:
                observation = f"Error: Unknown tool '{action_name}'"
                
            print(f"  [Observation]: {observation}\n")
            
            # Format the observation and append it to our conversation history
            messages.append({"role": "user", "content": f"Observation: {observation}"})
        else:
            # Error handling if the model fails to follow instructions
            messages.append({"role": "user", "content": "Error: You must provide a valid Action and Action Input or a Final Answer."})

    print("\n>>> Reached maximum steps without finding a final answer.")
    return "Error: Max steps reached."

# 4. Example Query Execution
if __name__ == "__main__":
    # Test Query showing multi-hop reasoning
    query = "Who is the CEO of OpenAI and what is his birth year?"
    
    print("WARNING: Make sure you have set 'OPENAI_API_KEY' in your environment or code.")
    print("Running demonstration...")
    
    # Please uncomment code below when running the script directly
    # react_agent(query)
