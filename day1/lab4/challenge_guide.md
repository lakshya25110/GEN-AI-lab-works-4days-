# Lab 4: Prompt Engineering Challenge

Welcome to the grand finale: **Lab 4**. The goal of this challenge is to apply all three advanced prompting patterns you've learned to a practical, real-world scenario: building an enterprise-grade **Customer Support Chatbot**.

## The Challenge
A basic Support Chatbot just answers regurgitated text. A *smart* support chatbot can:
1. Use **Chain of Thought (CoT)** to analyze the customer's sentiment and intent before replying.
2. Use **ReAct** to query external databases (e.g., retrieving shipping data) rather than guessing.
3. Use **Self-Reflection** to double-check its own tone, ensuring it responds politely and accurately before the message is sent to the customer.

## Pattern 1: Chain of Thought (CoT) in Support
If a customer writes "My delivery is 3 days late and I'm furious, this is the worst service ever!", a CoT prompt forces the model to slow down:
*Prompt Engineering:* "First, analyze the user's sentiment carefully. Second, identify the core request. Third, formulate your reply."
*Result:* The bot reasons out the anger, realizes the core request is looking for a package, and replies with deep empathy.

## Pattern 2: ReAct in Support
Instead of making up a tracking number, you give the bot a `check_order_status` tool.
*Prompt Engineering:* "If the user asks about an order, ALWAYS output Action: check_order_status."
*Result:* The bot acts as an agent, querying shipping APIs before constructing its sentence.

## Pattern 3: Self-Reflection in Support
We introduce a "Reviewer" prompt alongside the "Creator". 
*Prompt Engineering:* "You are a Quality Assurance bot. Read the draft reply below. Is it polite? Does it solve the issue? If not, rewrite it."
*Result:* Drafts that are accidentally robotic or rude get caught by the reflection system and rewritten.

## Your Workbench
In your workspace (`lab4_prompt_challenge`), you have access to a Streamlit application (`app.py`) that acts as a Prompt Engineering Playground. You can toggle between these three patterns and observe how drastically the system prompt dictates the AI's behavior!
