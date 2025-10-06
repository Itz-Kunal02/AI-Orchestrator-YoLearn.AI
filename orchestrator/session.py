"""Session management and user profiles"""

from typing import Dict, Optional
from datetime import datetime

# In-memory session storage
SESSIONS: Dict[str, Dict] = {}

def init_session(user_id: str, session_id: Optional[str] = None) -> str:
    """Initialize or retrieve user session"""
    if not session_id:
        session_id = f"{user_id}_{int(datetime.now().timestamp())}"
    
    if session_id not in SESSIONS:
        SESSIONS[session_id] = {"history": [], "profile": {}}
    
    return session_id

def _default_user() -> Dict:
    """Generate default user profile"""
    return {
        "user_id": "student_demo",
        "name": "Demo Student",
        "grade_level": "10",
        "learning_style_summary": "Structured learner",
        "emotional_state_summary": "Engaged",
        "mastery_level_summary": "Level 5: Developing"
    }
