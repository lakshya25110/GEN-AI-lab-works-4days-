# Lab 3: Self-Reflecting Code Review Agent

Welcome to Lab 3! In this lab, we step up from standard prompting and introduces a powerful concept in agentic architectures: **Self-Reflection**. 

You will build an agent that reviews Python code, generates a corrected version, and then computationally checks its own work using Python's built-in `ast` (Abstract Syntax Tree) module. If the agent makes a syntax mistake, it catches the error and iterates to fix it automatically!

## 1. What is Self-Reflection?
Standard code generation is "one-shot": 
- User: "Write a function." 
- LLM: "Here is the code." (If the code is broken, it fails).

**Self-Reflection** introduces an iterative loop where the AI acts as both the *Creator* and the *Reviewer*. 
1. The AI generates the initial code.
2. A deterministic tool (in this case, an internal Python syntax checker) evaluates the code.
3. If an error is found, the error trace is passed *back* to the AI.
4. The AI reflects on the error, understands what went wrong, and generates V2 of the code.

This significantly increases the reliability of agentically generated code because the model is verifying its work against ground truth systems before showing the final result.

## 2. Using Python's `ast` Module
To test if Python code is valid without dangerously running unknown code (`exec` or `eval`), we can use the Abstract Syntax Tree module (`ast`). 

```python
import ast

def is_valid_python(code_string):
    try:
        ast.parse(code_string)
        return True, "Code is valid."
    except SyntaxError as e:
        return False, f"SyntaxError on line {e.lineno}: {e.msg}"
```
If `ast.parse` succeeds, we know the code has zero syntax indentation or missing colon errors. If it fails, we trap the exact error line and message and send it straight back to the LLM!

## 3. The Reflection Loop
We implement this via a loop with a fixed maximum number of iterations (e.g., 3).

1. **Attempt 1:** The LLM receives the user's messy code and returns a code block of cleaned up code.
2. Our Python script extracts that code block and runs `ast.parse()`.
3. **If Valid:** Break the loop and present the code to the user.
4. **If Invalid:** Append a message to the chat history: `Observation: The code you provided raised a SyntaxError...` and loop!

## 4. Implementation Details
In your workspace, you will find:
- **`reviewer.py`**: The core execution loop combining the Groq LLM API and the `ast` parser.
- **`app.py`**: The visual Streamlit application that lets you see the reflection iterations happening in real-time.
