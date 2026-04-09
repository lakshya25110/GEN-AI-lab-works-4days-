import re
import ast
from openai import OpenAI

def extract_python_code(llm_output):
    """
    Helper function to extract code inside ```python ``` blocks.
    Returns the raw string if no block is found.
    """
    match = re.search(r"```python\n(.*?)\n```", llm_output, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1)
    return llm_output

def check_syntax_with_ast(code):
    """
    Validates Python syntax safely without executing the code.
    Returns (is_valid, message).
    """
    try:
        ast.parse(code)
        return True, "Code passed AST syntax validation."
    except SyntaxError as e:
        return False, f"SyntaxError at line {e.lineno}, offset {e.offset}: {e.msg}\nCode snippet causing error:\n{e.text}"
    except Exception as e:
        return False, f"Error validating code: {str(e)}"

def self_reflecting_reviewer(user_code, api_key, model="llama-3.1-8b-instant", base_url="https://api.groq.com/openai/v1"):
    """
    The Core Agent Logic.
    Takes user code, reviews it, writes a new version, checks it with AST, and iteratively fixes it.
    This function acts as an iterator, yielding steps so the UI can stream updates.
    """
    client = OpenAI(api_key=api_key, base_url=base_url)
    
    system_prompt = """
    You are an Expert Python Code Review Agent.
    Your job is to repair buggy, inefficient, or un-pythonic code.
    
    1. Provide a brief review of what was wrong.
    2. Provide the corrected code.
    
    You MUST wrap your corrected code entirely inside a ```python ``` markdown block so the system parser can extract it.
    If the system tells you the code raised a SyntaxError, you must analyze the error and output a FIXED version of the code inside a new python code block.
    """
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Please review and fix this python code:\n\n{user_code}"}
    ]
    
    max_reflections = 3 # Prevent infinite loops
    
    for attempt in range(max_reflections):
        yield {"status": f"Agent is analyzing (Attempt {attempt + 1})...", "type": "info"}
        
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.2 # low temp for code generation
            )
        except Exception as e:
            yield {"status": f"API Error: {str(e)}", "type": "error", "done": True}
            return
            
        ass_msg = response.choices[0].message.content
        messages.append({"role": "assistant", "content": ass_msg})
        
        # Extract and check the code
        extracted_code = extract_python_code(ass_msg)
        yield {"status": "Agent generated code. Extracting and validating AST...", "type": "info", "raw": ass_msg}
        
        is_valid, validation_msg = check_syntax_with_ast(extracted_code)
        
        if is_valid:
            yield {
                "status": "Success! The code passed syntax validation.", 
                "type": "success", 
                "final_code": extracted_code,
                "full_response": ass_msg,
                "done": True
            }
            return
        else:
            yield {
                "status": f"Validation Failed: {validation_msg}", 
                "type": "warning",
                "extracted": extracted_code
            }
            # Add the critique back to the message history so the model reflects on it
            critique = f"System Observation: The parsed code raised a syntax error.\n{validation_msg}\n\nPlease reflect on this error and output a fully fixed version wrapped in ```python ... ```."
            messages.append({"role": "user", "content": critique})
            
    # If the loop exhausts
    yield {
        "status": "Reached maximum reflection iterations without producing valid code.", 
        "type": "error", 
        "full_response": messages[-1]["content"],
        "done": True
    }
