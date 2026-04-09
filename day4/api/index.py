import os
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# 🛠️ Add parent directory to path so we can import from the root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import run_blog_crew

app = FastAPI()

class BlogRequest(BaseModel):
    topic: str
    audience: Optional[str] = "Professional"
    tone: Optional[str] = "Informative"
    model_name: Optional[str] = "groq/llama-3.3-70b-versatile"

@app.get("/api")
def hello_world():
    return {"status": "recognized", "message": "Blog Crew API is operational"}

@app.post("/api/generate")
async def generate_blog(request: BlogRequest):
    try:
        # Run the CrewAI logic
        result = run_blog_crew(
            topic=request.topic,
            audience=request.audience,
            tone=request.tone,
            model_name=request.model_name
        )
        return {"status": "success", "blog_post": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Entry point for Vercel
app = app
