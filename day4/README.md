# ✍️ Blog Generation Team (CrewAI)

A professional 3-agent editorial team designed to research, write, and edit high-quality blog posts autonomously.

## 🤖 The Editorial Team
1. **Researcher**: Gathers data and breakthroughs on the topic.
2. **Writer**: Drafts the blog post based on research context.
3. **Editor**: Polishes for clarity, tone, and SEO.

## 🛠️ Setup
1. Open your terminal in `folder2/blog_crew`.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your environment variables:
   - `OPENAI_API_KEY`: Your OpenAI key.
   - `SERPER_API_KEY` (Optional): For web search.
   - `TAVILY_API_KEY` (Optional): Alternative search tool.

## 🚀 How to Run
Run the main script:
```bash
python main.py
```
Enter your topic when prompted. The final blog post will be automatically saved as a `.md` file in this directory.

## ✨ Features
- **Sequential Flow**: Agents share context automatically.
- **Auto-Save**: Final outputs are saved as markdown for easy publishing.
- **Factual Accuracy**: Triage and Editing tasks explicitly check for research alignment.
