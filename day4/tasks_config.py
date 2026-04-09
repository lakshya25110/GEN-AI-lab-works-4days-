from crewai import Task

def get_tasks(researcher, writer, editor, topic: str):
    """Define and return the sequential tasks for the editorial team."""

    # 1. Research Task
    research_task = Task(
        description=(
            f"Thoroughly research the topic: {topic}. "
            "Identify the latest trends, key players, and significant technical or social breakthroughs. "
            "Find specific facts, statistics, and expert opinions that can be used as evidence in the blog post. "
            "Ensure the information is from verifiable sources to minimize hallucinations."
        ),
        expected_output=(
            "A comprehensive research report containing: \n"
            "- A summary of the current landscape of the topic. \n"
            "- 5-7 key facts or breakthroughs. \n"
            "- A list of relevant technical concepts explained simply. \n"
            "- References to sources or trends identified."
        ),
        agent=researcher
    )

    # 2. Writing Task
    writing_task = Task(
        description=(
            f"Using the research report, write an engaging and professional blog post about {topic}. "
            "The post should be structured with a catchy title, an introduction that hooks the reader, "
            "several section headers for readability, and a strong conclusion with a call-to-action. "
            "Target Audience: Professional audience interested in technology and innovation. "
            "Tone: Informative, forward-thinking, and authoritative."
        ),
        expected_output=(
            "A complete draft of the blog post in Markdown format. "
            "The draft must be between 800 and 1200 words and include at least 3 subheadings."
        ),
        agent=writer,
        context=[research_task] # Important: writer needs the research
    )

    # 3. Editing Task
    editing_task = Task(
        description=(
            "Review and polish the blog post draft. Check for grammar, clarity, and narrative flow. "
            "Ensure that the tone is consistent and professional. optimize the content for SEO "
            "by ensuring keywords related to the topic are used naturally in headers and body text. "
            "Finally, verify that all facts mentioned in the post align with the research provided."
        ),
        expected_output=(
            "A final, publish-ready blog post in Markdown format. "
            "Include a suggested SEO Meta Description at the end of the post."
        ),
        agent=editor,
        context=[writing_task, research_task] # Editor checks writing against research
    )

    return [research_task, writing_task, editing_task]
