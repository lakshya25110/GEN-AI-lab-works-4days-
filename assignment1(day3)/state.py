from typing import TypedDict, List, Optional, Dict
from pydantic import BaseModel, Field

class CandidateInfo(BaseModel):
    name: str = Field(description="Name of the candidate")
    email: str = Field(description="Email address")
    skills: List[str] = Field(description="List of key skills")
    experience_years: float = Field(description="Years of relevant experience")
    education: str = Field(description="Highest degree or education background")

class InterviewSlot(BaseModel):
    date: str
    time: str

class AgentState(TypedDict):
    resume_text: str
    job_description: str
    candidate_info: Optional[CandidateInfo]
    screening_score: Optional[int]
    is_shortlisted: bool
    interview_scheduled: bool
    interview_slot: Optional[Dict]
    interview_feedback: Optional[str]
    final_score: Optional[int]
    hiring_recommendation: Optional[str]
    current_node: str
    error: Optional[str]
