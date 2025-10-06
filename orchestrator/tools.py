"""Educational tool execution"""

from typing import Dict, Any
from .models import ToolExecution

# Tool schema definitions
TOOL_SCHEMAS = {
    "quiz_generator": {
        "defaults": {
            "difficulty": "beginner",
            "question_type": "practice",
            "num_questions": 5
        }
    },
    "concept_explainer": {
        "defaults": {
            "desired_depth": "basic"
        }
    },
    "note_maker": {
        "defaults": {
            "note_taking_style": "structured",
            "include_examples": True
        }
    },
    "flashcard_generator": {
        "defaults": {
            "count": 5,
            "difficulty": "medium",
            "include_examples": True
        }
    }
}

def pick_tool_from_intent(intent: str) -> str:
    """Select appropriate tool based on intent"""
    intent_lower = intent.lower()
    
    if "practice" in intent_lower or "quiz" in intent_lower or "problems" in intent_lower:
        return "quiz_generator"
    if "note" in intent_lower or "summary" in intent_lower:
        return "note_maker"
    if "explain" in intent_lower or "explanation" in intent_lower:
        return "concept_explainer"
    
    return "quiz_generator"  # Default

async def call_tool(tool_name: str, params: Dict[str, Any]) -> ToolExecution:
    """Execute selected educational tool"""
    
    if tool_name == "quiz_generator":
        raw = f"Generated {params['num_questions']} {params['difficulty']} questions on {params['topic']}"
    else:
        raw = f"Explained concept {params['topic']} at {params['difficulty']} depth"
    
    return ToolExecution(
        tool_name=tool_name,
        request_params=params,
        raw_tool_response=raw,
        formatted_response=raw
    )
