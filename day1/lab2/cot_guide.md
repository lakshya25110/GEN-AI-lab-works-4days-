# Chain of Thought (CoT) Lab: Solving Math Problems

Welcome to Lab 2! In this module, we explore the **Chain of Thought (CoT)** prompting technique. You will learn how to drastically improve the mathematical reasoning capabilities of Large Language Models by forcing them to "think out loud" before producing an answer.

## 1. What is Chain of Thought?
Standard prompting asks the LLM for a direct answer:
*Prompt:* "If I have 5 apples, eat 2, and buy 4 more, how many do I have?"
*Direct Answer:* "7"

While this might work for simple arithmetic, LLMs often fail at complex, multi-step word problems. 

**Chain of Thought** prompting solves this by structuring the prompt so the LLM outputs reasoning steps before the final answer.
*Prompt:* "Let's think step-by-step. If I have 5 apples, eat 2, and buy 4 more, how many do I have?"
*CoT Answer:* 
"Step 1: I start with 5 apples.
Step 2: I eat 2 apples, leaving 5 - 2 = 3 apples.
Step 3: I buy 4 more apples, giving me 3 + 4 = 7 apples.
Final Answer: 7"

By expanding the context window with intermediate logical steps, the LLM has a significantly higher chance of arriving at the correct final answer.

## 2. Implementation Approach
To implement CoT for math problems, we don't necessarily need external tools like search or calculators (though they help). We primarily need effective **Prompt Engineering**.

### Zero-Shot CoT
Adding the magic phrase *"Let's think step by step"* to the end of a prompt.

### Few-Shot CoT
Providing the LLM with a couple of examples of how you want it to reason mathematically. For example:
```
Q: Roger has 5 tennis balls. He buys 2 more cans of tennis balls. Each can has 3 tennis balls. How many tennis balls does he have now?
A: Roger started with 5 balls. 2 cans of 3 tennis balls each is 6 tennis balls. 5 + 6 = 11. The answer is 11.

Q: The cafeteria had 23 apples. If they used 20 to make lunch and bought 6 more, how many apples do they have?
```

## 3. Python Implementation
In this lab, we build a Python script (`cot_math.py`) and a Streamlit UI (`app.py`) that uses a system prompt designed to enforce mathematical CoT.

### The System Prompt used in this Lab:
```text
You are an expert mathematical problem solver.
When given a math problem, you MUST first explain your logic step-by-step using a Chain-of-Thought process.
Only after fully walking through the steps should you provide the Final Answer.

Format your response exactly as follows:

Reasoning:
<your step-by-step logic here>

Final Answer:
<the final numerical answer here>
```

This strict formatting makes it easy for us to parse the output and display the reasoning process visually in our application!
