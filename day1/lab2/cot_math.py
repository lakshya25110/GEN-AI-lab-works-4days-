import os
import re
from openai import OpenAI

def solve_math_problem(problem, api_key, model="llama-3.1-8b-instant", base_url="https://api.groq.com/openai/v1"):
    """
    Solves a math problem using the Chain of Thought pattern.
    Default configuration uses Groq's servers and the Llama 3 API since it's blazingly fast.
    """
    
    # We initialize the client inside the function so it captures the UI's API key
    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )
    
    system_prompt = """
    You are an expert mathematical problem solver. 
    When given a math problem, you MUST first explain your logic step-by-step using a Chain-of-Thought process before providing the final answer.
    
    Structure your response EXACTLY like this:
    
    Reasoning:
    <write out your step-by-step mathematical reasoning here>
    
    Final Answer:
    <a single sentence containing just the final concise mathematical answer>
    """
    
    # We use explicit CoT prompting in the user message as well (Zero-Shot CoT)
    user_prompt = f"Problem: {problem}\n\nPlease solve this by thinking step-by-step."
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.0 # Zero temperature for math tasks is crucial for logic stability
        )
        
        output = response.choices[0].message.content
        return output
        
    except Exception as e:
        return f"Error: {str(e)}"

def parse_cot_output(raw_output):
    """
    Parses the raw output to separate the reasoning from the final answer.
    """
    # Regex to capture the reasoning and final answer
    reasoning_match = re.search(r"Reasoning:\s*(.*?)\nFinal Answer:", raw_output, re.IGNORECASE | re.DOTALL)
    answer_match = re.search(r"Final Answer:\s*(.*)", raw_output, re.IGNORECASE | re.DOTALL)
    
    reasoning = reasoning_match.group(1).strip() if reasoning_match else raw_output
    final_answer = answer_match.group(1).strip() if answer_match else "Could not isolate final answer."
    
    return {
        "reasoning": reasoning,
        "final_answer": final_answer,
        "raw": raw_output
    }

if __name__ == "__main__":
    # Test script via console
    mock_problem = "I have a 10 liter jug and a 3 liter jug. I need exactly 4 liters of water. How do I do it?"
    print(f"Problem: {mock_problem}")
    print("WARNING: You must set your API key to run this directly in console.")
    # result = solve_math_problem(mock_problem, os.environ.get("OPENAI_API_KEY"))
    # print(result)
