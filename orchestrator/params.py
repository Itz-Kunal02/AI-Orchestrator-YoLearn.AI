# orchestrator/params.py

from typing import Dict, Any, List, Optional, Tuple
from .tools import pick_tool_from_intent
from .models import UserInfo, ChatMessage

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

    # Build user_info
    if user_info:
        user_info_obj = UserInfo(**user_info)
    else:
        user_info_obj = UserInfo(
            user_id="student_demo",
            name="Demo Student",
            grade_level="10",
            learning_style_summary="Structured learner",
            emotional_state_summary=f"Currently feeling {emotion}",
            mastery_level_summary="Level 5: Developing"
        )

    # Convert chat history entries
    chat_msgs = []
    if chat_history:
        for entry in chat_history[-5:]:
            chat_msgs.append(ChatMessage(role=entry["role"], content=entry["message"]))

    # Default settings
    defaults = {
        "quiz_generator": {"difficulty": "beginner", "question_type": "practice", "num_questions": 5},
        "flashcard_generator": {"count": 5, "difficulty": "medium", "include_examples": True},
        "note_maker": {"note_taking_style": "structured", "include_examples": True, "include_analogies": False},
        "concept_explainer": {"desired_depth": "basic"}
    }
    tool_defaults = defaults.get(tool, {})

    # Emotional adaptation
    diff = tool_defaults.get("difficulty", "medium")
    if emotion in ["confused", "anxious", "frustrated"]:
        diff = "easy"
    elif emotion == "confident":
        diff = "hard"

    # Build params per tool
    if tool == "quiz_generator":
        params = {
            "user_info": user_info_obj.dict(),
            "topic": topic,
            "difficulty": diff,
            "question_type": tool_defaults.get("question_type"),
            "num_questions": tool_defaults.get("num_questions")
        }
    elif tool == "flashcard_generator":
        count = tool_defaults.get("count", 5)
        params = {
            "user_info": user_info_obj.dict(),
            "topic": topic,
            "count": count,
            "difficulty": diff,
            "subject": topic.split()[0],
            "include_examples": tool_defaults.get("include_examples", True)
        }
    elif tool == "note_maker":
        params = {
            "user_info": user_info_obj.dict(),
            "chat_history": [msg.dict() for msg in chat_msgs],
            "topic": topic,
            "subject": topic.split()[0],
            "note_taking_style": tool_defaults.get("note_taking_style"),
            "include_examples": tool_defaults.get("include_examples", True),
            "include_analogies": tool_defaults.get("include_analogies", False)
        }
    elif tool == "concept_explainer":
        params = {
            "user_info": user_info_obj.dict(),
            "chat_history": [msg.dict() for msg in chat_msgs],
            "concept_to_explain": topic,
            "current_topic": topic.split()[0],
            "desired_depth": tool_defaults.get("desired_depth", "basic")
        }
    else:
        # Fallback
        params = {"topic": topic}

    return tool, params
