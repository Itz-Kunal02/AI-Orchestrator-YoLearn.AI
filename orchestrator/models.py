"""Pydantic models for request/response validation"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class OrchestratorRequest(BaseModel):
    user_input: str
    user_id: str
    session_id: Optional[str] = None

class OrchestratorResponse(BaseModel):
    success: bool
    response: str
    intent: str
    topic: str
    emotional_state: str
    suggestions: List[str] = []

class ToolExecution(BaseModel):
    tool_name: str
    request_params: Dict[str, Any]
    raw_tool_response: Any
    formatted_response: str

class FullOrchestratorResponse(OrchestratorResponse):
    tool_execution: ToolExecution
    session_id: str
    next_actions: List[str]

def generate_suggestions(intent: str, emotion: str) -> List[str]:
    """Generate adaptive suggestions based on intent and emotion"""
    suggestions = []
    
    if "practice" in intent or "problems" in intent:
        suggestions.extend([
            "Generate flashcards for practice",
            "Provide concise notes summary",
            "Ask for detailed concept explanation"
        ])
    
    if emotion in ["confused", "anxious", "frustrated"]:
        suggestions.append("Break content into simpler parts")
    
    return suggestions[:3]
