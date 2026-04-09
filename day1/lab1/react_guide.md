# ReAct Agent Lab: Building a Reasoning & Acting LLM System

Welcome to the ReAct Agent Lab! In this module, you will learn how to build an advanced AI agent using the **ReAct (Reasoning + Acting)** pattern. This hands-on lab takes you from prompt engineering theory to a fully functional agent that can reason through complex questions and search the web for real-time information.

## 1. What is ReAct?
Standard Large Language Models (LLMs) can only generate text based on their static training data. When faced with complex, multi-step problems or questions requiring up-to-date knowledge, they often hallucinate or fail.

**ReAct** is a prompting framework that solves this by forcing the LLM to output its thought process alongside actions it wants to take. The loop works like this:
1. **Thought:** The model reasons about what it needs to do next.
2. **Action/Action Input:** The model decides to use a specific tool (e.g., Search) and provides the input.
3. **Observation:** Our Python code executes the tool and hands the result back to the LLM.
4. **Repeat:** The loop continues until the LLM reasons it has the final answer.

**Why is this important?** 
ReAct brings autonomy to LLMs. Instead of hardcoding logic, you provide tools, and the LLM figures out how to use them to solve the problem dynamically.

---

## 2. Step-by-Step Implementation

### Step 1: Setting up the Environment
Ensure you have the required libraries installed:
```bash
pip install openai requests
```
You will also need an OpenAI API key. Set it in your environment:
```python
import os
os.environ["OPENAI_API_KEY"] = "sk-..."
```

### Step 2: Defining the Loop Structure
The core of a ReAct agent is a `while` loop. 
- You pass the prompt to the LLM.
- If the LLM returns a final answer, you break the loop. 
- If it returns an action, you execute the tool, append the result to the conversation, and continue the loop.

### Step 3: Integrating the Tool (Web Search)
We need a function that performs an action. For this lab, we'll use a mock search function, but in production, you could plug in the Google Search API, Wikipedia API, or a custom database.
```python
def search_tool(query):
    # Mock implementation for the lab
    ...
```

### Step 4: Parsing Model Outputs
The standard way to guide the ReAct agent is via strict formatting rules in the system prompt. We tell the model to use the exact format:
```text
Thought: <reasoning>
Action: Search
Action Input: <query>
```
Using Python's regular expressions (`re`), we extract `Action` and `Action Input` so our code can run the tool.

---

## 3. The Implementation Code
You can find the full executable Python script in the workspace as `react_agent.py`. Here is a look at the core logic:

```python
import os
import re
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "your-api-key"))

# The System Prompt guiding the ReAct behavior
SYSTEM_PROMPT = """You are an intelligent agent that answers questions by reasoning and using tools.
You have access to the following tool:
Observation: <result of the search>

When you know the final answer, output it as:
Thought: I know the final answer.
Final Answer: <the answer>
"""

# ... (Check react_agent.py for the full implementation and loop logic)
```

---

## 4. Example Run

**User Query:** *"Who is the CEO of OpenAI and what is his birth year?"*

**Step 1:**
- **Thought:** I need to find out who the CEO of OpenAI is first.
- **Action:** Search
- **Action Input:** CEO of OpenAI

*Code executes search...*
- **Observation:** The CEO of OpenAI is Sam Altman.

**Step 2:**
- **Thought:** Now I know the CEO is Sam Altman. I need to find his birth year.
- **Action:** Search
- **Action Input:** Sam Altman birth year

*Code executes search...*
- **Observation:** Sam Altman was born in 1985.

**Step 3:**
- **Thought:** I now have both pieces of information: the CEO is Sam Altman, and his birth year is 1985. I can formulate the final answer.
- **Final Answer:** The CEO of OpenAI is Sam Altman, and he was born in 1985.

---

## 5. Key Learnings & Prompt Design Best Practices

1. **Chain of Thought (CoT):** Forcing the model to output a `Thought` before an `Action` dramatically improves reliability. It prevents the model from blindly guessing tool usage.
2. **Strict Formatting:** Notice how strict the formatting rules are in the system prompt. This makes parsing with regex in Python straightforward and resilient.
3. **Error Handling:** Always implement a `max_steps` counter in your loop. ReAct agents can sometimes get stuck in an infinite loop of repeated actions if they can't find the answer.
4. **Context Window Limitations:** Appending `Observation` outputs back into the context keeps the agent aware of past actions, but beware of long search results consuming your token limits.
