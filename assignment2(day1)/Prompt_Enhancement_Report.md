# Prompt Engineering: Quality Evaluation & Enhancement Report

As a senior prompt engineer and AI quality evaluator, I have analyzed five commonly used, poorly written prompts. Below, I demonstrate how to transform these vague requests into highly effective, structured prompts optimized for consistent, high-quality AI outputs.

## Prompt 1: The Vague Content Generation
### Before
Write a blog post about Artificial Intelligence.

### After
**Act as completely a senior technical copywriter.** Write a 500-word blog post about the impact of Artificial Intelligence on productivity in the modern workplace. 

**Target audience:** Small business owners with non-technical backgrounds. 
**Tone:** Professional, encouraging, and easy to understand. 

**Format Requirements:** 
- Use an engaging, click-worthy title.
- Structure with short paragraphs and bullet points where applicable.
- Provide 3 specific, actionable examples of AI use cases.
- **Constraint:** Do not use overly complex technical jargon; explain any necessary terms simply.

### Explanation
**What was wrong:** The original prompt is completely unconstrained, leading to generic, wildly variable outputs that lack a targeted audience, tone, or specific objective. 
**How it's fixed:** The improved prompt is highly specific. It assigns an expert role, defines the exact boundaries (productivity impact, 500 words), identifies the target audience to calibrate the complexity, sets a distinct tone, and applies specific formatting constraints to guarantee a scannable and practical output.

---

## Prompt 2: The Ambiguous Debugging Request
### Before
Fix the bugs in this code so it works.

### After
**Act as an expert Python developer.** Your objective is to debug the provided code snippet to resolve a 'KeyError' when processing dictionary keys.

**Step-by-step instructions:**
1. Analyze the given code to identify why the dictionary key lookup is failing.
2. Rewrite the code utilizing either the `.get()` method or a `try/except` block to handle missing keys gracefully.

**Output constraints:** 
- Return *only* the corrected exact code block.
- Follow the code block with a short bulleted list explaining exactly what was changed and the reasoning behind it. 
- Do not provide unrelated optimizations or conversational fluff.

### Explanation
**What was wrong:** The original prompt provides zero context regarding what the code is meant to do, what language it is written in, or what error is occurring. AI models often hallucinate "fixes" for non-existent bugs when given vague instructions.
**How it's fixed:** By assigning an expert persona and identifying the precise problem (KeyError exception) and language, the scope is immediately narrowed. Forcing a step-by-step approach ensures logical problem-solving, while rigorous output formatting constraints guarantee a clean, usable response without excessive "AI chatter."

---

## Prompt 3: The Unfocused Summarization
### Before
Summarize this text for me.

### After
**Act as an executive assistant.** Please read the provided meeting transcript and create a strictly structured summarizing brief.

**Requirements:**
1. **TL;DR:** Provide a one-sentence summary of the meeting's primary outcome.
2. **Decisions:** List 3 to 5 key decisions made, using bullet points.
3. **Action Items:** List any action items, explicitly noting the assigned person and the deadline for each.

**Constraints:** 
- Keep the entire output under 200 words. 
- Ignore minor tangents or pleasantries mentioned in the transcript. 
- Your output must strictly follow the format: TL;DR, Decisions, and Action Items.

### Explanation
**What was wrong:** "Summarize" allows the AI to choose its own summarization style, length, and focus. Often, it produces a block of text that misses critical operational details like deadlines or assignments.
**How it's fixed:** The enhancement dictates an exact formatting structure. It focuses the AI solely on actionable business intelligence (decisions, action items) rather than a narrative summary. Imposing a hard negative constraint ("Ignore minor tangents") prevents the model from wasting tokens on irrelevant information.

---

## Prompt 4: The Context-Free Brainstorming
### Before
Give me some ideas for a marketing campaign.

### After
**Act like a B2B digital marketing strategist.** Our company sells a cloud-based CRM tool aimed at mid-sized e-commerce businesses. Our explicit goal is to increase Q3 sign-ups by 15%.

Please provide exactly 3 distinct, actionable marketing campaign concepts. 

For each concept, outline the following strictly in this format:
- **Concept Name:**
- **Primary Audience Insight:**
- **Core Message/Hook:**
- **Recommended Channels:** (e.g., LinkedIn, Email, SEO)

**Constraints:** 
- Focus exclusively on digital strategies requiring low initial capital. 
- Avoid generic, overused suggestions like "host a social media giveaway."

### Explanation
**What was wrong:** Brainstorming prompts fail predictably when they lack business constraints and situational context, resulting in generic, unimplementable ideas.
**How it's fixed:** The improved version grounds the AI in reality by establishing the business vertical (B2B SaaS), target market, and measurable goals. Limiting the output to 3 ideas forces prioritization of quality over volume. The required outline structure guarantees that each resulting idea is immediately actionable and evaluated against the strategic objective.

---

## Prompt 5: The Blind Translation
### Before
Translate this document into Spanish.

### After
**Act as a professional localized technical translator.** Translate the provided user manual excerpt for a medical device from English to Mexican Spanish.

**Guidelines:**
- Maintain a highly formal, precise, and authoritative tone suitable for medical professionals.
- Ensure all technical terms adhere accurately to standardized medical terminology.
- **Critical Rule:** Do not localize or translate the brand name "AeroFlow". Leave it exactly as written.
- **Structure:** Output the final translation paragraph by paragraph, exactly matching the formatting (headers, bullet spacing) of the source text.

### Explanation
**What was wrong:** Standard translation prompts force the AI to guess regional dialects, appropriate tone, and formatting constraints. For specialized documents, this can lead to catastrophic inaccuracies.
**How it's fixed:** The enhanced prompt solves this ambiguity by declaring the precise regional dialect (Mexican Spanish), and defining the target audience to dictate the tone (formal, medical). Providing explicit negative rules for brand-name terminology prevents unwanted alterations, and structural guidelines ensure the output is ready to be directly copy-pasted into the destination system.
