"""Parameter extraction and tool configuration"""

from typing import Dict, Any, List, Optional, Tuple
from .tools import pick_tool_from_intent, TOOL_SCHEMAS

def extract_tool_params(
    intent: str, 
    topic: str, 
    emotion: str, 
    user_info: Optional[Dict] = None, 
    chat_history: Optional[List] = None
) -> Tuple[str, Dict[str, Any]]:
    """Extract and configure parameters for selected tool"""
    
    # Select tool
    tool = pick_tool_from_intent(intent)
    
    # Get defaults
    defaults = TOOL_SCHEMAS[tool]["defaults"]
    params = dict(defaults)
    
    # Extract subject
    subject = topic.split()[0] if topic else "general"
    
    # Adjust difficulty based on emotion
    difficulty = params.get("difficulty", "medium")
    if emotion in ["confused", "anxious", "frustrated"]:
        difficulty = "easy"
    elif emotion == "confident":
        difficulty = "hard"
    
    # Configure tool-specific parameters
    if tool == "quiz_generator":
        params.update({
            "topic": topic,
            "subject": subject,
            "difficulty": difficulty,
            "question_type": params.get("question_type"),
            "num_questions": params.get("num_questions")
        })
    elif tool == "concept_explainer":
        params.update({
            "user_info": user_info,
            "chat_history": chat_history,
            "concept_to_explain": topic,
            "current_topic": subject,
            "desired_depth": "basic" if difficulty == "easy" else "intermediate"
        })
    
    return tool, params
