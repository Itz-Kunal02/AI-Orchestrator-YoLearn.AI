"""Enhanced parameter extraction with proper schema mapping"""

from typing import Dict, Any, List, Optional, Tuple
from .tools import pick_tool_from_intent, TOOL_SCHEMAS
from .models import UserInfo, ChatMessage

def extract_tool_params(
    intent: str, 
    topic: str, 
    emotion: str, 
    user_info: Optional[Dict] = None, 
    chat_history: Optional[List] = None
) -> Tuple[str, Dict[str, Any]]:
    """Extract and configure parameters for selected tool with proper schema validation"""
    
    # Select tool
    tool = pick_tool_from_intent(intent)
    
    # Create proper user_info object
    if user_info:
        user_info_obj = UserInfo(**user_info)
    else:
        # Create default user info with emotional adaptation
        emotion_summary = f"Currently feeling {emotion}"
        if emotion == "frustrated":
            emotion_summary += " and needs encouragement"
        elif emotion == "confident":
            emotion_summary += " and ready for challenges"
        
        user_info_obj = UserInfo(
            user_id="demo_student",
            name="Demo Student",
            grade_level="10",
            learning_style_summary="Prefers structured learning with examples",
            emotional_state_summary=emotion_summary,
            mastery_level_summary="Level 5: Developing competence"
        )
    
    # Convert chat history
    chat_messages = []
    if chat_history:
        for msg in chat_history[-5:]:  # Last 5 messages
            if isinstance(msg, dict):
                chat_messages.append(ChatMessage(
                    role="user",  # Simplified for demo
                    content=msg.get("message", "")
                ))
    
    # Get defaults and adapt based on emotion
    defaults = TOOL_SCHEMAS.get(tool, {}).get("defaults", {})
    
    # Emotional intelligence adjustments
    difficulty = defaults.get("difficulty", "medium")
    if emotion in ["confused", "anxious", "frustrated"]:
        difficulty = "easy"
    elif emotion == "confident":
        difficulty = "hard"
    
    # Tool-specific parameter extraction
    if tool == "note_maker":
        params = {
            "user_info": user_info_obj.dict(),
            "chat_history": [msg.dict() for msg in chat_messages],
            "topic": topic,
            "subject": topic.split('_')[0] if '_' in topic else topic.split()[0] if topic else "general",
            "note_taking_style": defaults.get("note_taking_style", "structured"),
            "include_examples": defaults.get("include_examples", True),
            "include_analogies": emotion in ["confused", "frustrated"]  # More analogies when struggling
        }
        
    elif tool == "flashcard_generator":
        count = defaults.get("count", 5)
        if emotion == "frustrated":
            count = min(count, 3)  # Fewer cards when frustrated
        elif emotion == "confident":
            count = min(count + 2, 10)  # More cards when confident
            
        params = {
            "user_info": user_info_obj.dict(),
            "topic": topic,
            "count": count,
            "difficulty": difficulty,
            "subject": topic.split('_')[0] if '_' in topic else topic.split()[0] if topic else "general",
            "include_examples": defaults.get("include_examples", True)
        }
        
    elif tool == "concept_explainer":
        depth_mapping = {
            "easy": "basic",
            "medium": "intermediate", 
            "hard": "advanced"
        }
        
        params = {
            "user_info": user_info_obj.dict(),
            "chat_history": [msg.dict() for msg in chat_messages],
            "concept_to_explain": topic,
            "current_topic": topic.split('_')[0] if '_' in topic else topic.split()[0] if topic else "general",
            "desired_depth": depth_mapping.get(difficulty, "basic")
        }
        
    else:
        # Fallback for quiz_generator (legacy)
        params = {
            "topic": topic,
            "subject": topic.split('_')[0] if '_' in topic else topic.split()[0] if topic else "general",
            "difficulty": difficulty,
            "question_type": defaults.get("question_type", "practice"),
            "num_questions": defaults.get("num_questions", 5)
        }
    
    return tool, params
