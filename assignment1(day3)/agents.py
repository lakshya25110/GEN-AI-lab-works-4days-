import json
from typing import Dict, Any
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from state import AgentState, CandidateInfo

class RecruitmentAgents:
    def __init__(self, api_key: str, model: str = "llama-3.1-70b-versatile"):
        self.llm = ChatGroq(api_key=api_key, model=model, temperature=0)

    def screen_resume(self, state: AgentState) -> Dict[str, Any]:
        """Agent 1: Resume Screening. Extracts info and scores candidate."""
        resume_text = state.get("resume_text", "")
        jd = state.get("job_description", "")
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert HR Recruitment Specialist. Extract candidate information and score the candidate based on the job description. Return JSON format with fields: name, email, skills, experience_years, education, and screening_score (0-100)."),
            ("user", f"Job Description:\n{jd}\n\nResume Content:\n{resume_text}")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({})
        
        try:
            # Simple cleanup for JSON
            content = response.content.strip()
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            data = json.loads(content)
            
            candidate_info = CandidateInfo(
                name=data.get("name", "Unknown"),
                email=data.get("email", "Unknown"),
                skills=data.get("skills", []),
                experience_years=float(data.get("experience_years", 0)),
                education=data.get("education", "Unknown")
            )
            score = int(data.get("screening_score", 0))
            
            return {
                "candidate_info": candidate_info,
                "screening_score": score,
                "is_shortlisted": score >= 60,
                "current_node": "Resume Screening"
            }
        except Exception as e:
            return {"error": f"Screening failed: {str(e)}", "current_node": "Resume Screening Error"}

    def schedule_interview(self, state: AgentState) -> Dict[str, Any]:
        """Agent 2: Interview Scheduling. Simulates matching slots."""
        if not state.get("is_shortlisted"):
            return {"current_node": "End (Rejected)"}
            
        # Simulated logic: available slots
        slots = [
            {"date": "2024-04-15", "time": "10:00 AM"},
            {"date": "2024-04-15", "time": "02:00 PM"},
            {"date": "2024-04-16", "time": "11:00 AM"}
        ]
        
        # In a real app, this might involve another agent or a tool call
        selected_slot = slots[0] 
        
        return {
            "interview_scheduled": True,
            "interview_slot": selected_slot,
            "current_node": "Interview Scheduling"
        }

    def evaluate_candidate(self, state: AgentState) -> Dict[str, Any]:
        """Agent 3: Candidate Evaluation. Final score and recommendation."""
        candidate = state.get("candidate_info")
        jd = state.get("job_description")
        
        # Simulate interview feedback (in a real system, this comes from a human or another node)
        feedback = "The candidate demonstrated strong technical knowledge but could improve communication skills."
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a Senior Technical Interviewer. Analyze the candidate info and interview feedback against the Job Description. Assign a final score (0-100) and a hiring recommendation (Strong Hire, Hire, Waitlist, or Reject). Return JSON."),
            ("user", f"JD: {jd}\nCandidate: {candidate}\nFeedback: {feedback}")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({})
        
        try:
            content = response.content.strip()
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            data = json.loads(content)
            
            return {
                "interview_feedback": feedback,
                "final_score": int(data.get("final_score", 0)),
                "hiring_recommendation": data.get("hiring_recommendation", "Reject"),
                "current_node": "Candidate Evaluation"
            }
        except Exception as e:
            return {"error": f"Evaluation failed: {str(e)}", "current_node": "Evaluation Error"}
