"""Enhanced Pydantic models with real tool schemas"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any, Literal
from enum import Enum

class OrchestratorRequest(BaseModel):
    user_input: str
    user_id: str
    session_id: Optional[str] = None

class UserInfo(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the student")
    name: str = Field(..., description="Student's full name")
    grade_level: str = Field(..., description="Student's current grade level")
    learning_style_summary: str = Field(..., description="Summary of student's preferred learning style")
    emotional_state_summary: str = Field(..., description="Current emotional state of the student")
    mastery_level_summary: str = Field(..., description="Current mastery level description")

class ChatMessage(BaseModel):
    role: Literal["user", "assistant"] = Field(..., description="Role of the message sender")
    content: str = Field(..., description="Content of the message")

# Tool Request Models
class NoteMakerRequest(BaseModel):
    user_info: UserInfo
    chat_history: List[ChatMessage]
    topic: str = Field(..., description="The main topic for note generation")
    subject: str = Field(..., description="Academic subject area")
    note_taking_style: Literal["outline", "bullet_points", "narrative", "structured"]
    include_examples: bool = True
    include_analogies: bool = False

class FlashcardGeneratorRequest(BaseModel):
    user_info: UserInfo
    topic: str = Field(..., description="The topic for flashcard generation")
    count: int = Field(..., ge=1, le=20, description="Number of flashcards to generate")
    difficulty: Literal["easy", "medium", "hard"]
    subject: str = Field(..., description="Academic subject area")
    include_examples: bool = True

class ConceptExplainerRequest(BaseModel):
    user_info: UserInfo
    chat_history: List[ChatMessage]
    concept_to_explain: str = Field(..., description="The specific concept to explain")
    current_topic: str = Field(..., description="Broader topic context")
    desired_depth: Literal["basic", "intermediate", "advanced", "comprehensive"]

# Tool Response Models
class NoteSection(BaseModel):
    title: str
    content: str
    key_points: List[str] = []
    examples: List[str] = []
    analogies: List[str] = []

class NoteMakerResponse(BaseModel):
    topic: str
    title: str
    summary: str
    note_sections: List[NoteSection]
    key_concepts: List[str]
    connections_to_prior_learning: List[str]
    visual_elements: List[Dict] = []
    practice_suggestions: List[str]
    source_references: List[str]
    note_taking_style: str

class Flashcard(BaseModel):
    title: str
    question: str
    answer: str
    example: Optional[str] = None

class FlashcardGeneratorResponse(BaseModel):
    flashcards: List[Flashcard]
    topic: str
    adaptation_details: str
    difficulty: str

class ConceptExplainerResponse(BaseModel):
    explanation: str
    examples: List[str]
    related_concepts: List[str]
    visual_aids: List[str]
    practice_questions: List[str]
    source_references: List[str]

# Enhanced Orchestrator Response
class ToolExecution(BaseModel):
    tool_name: str
    request_params: Dict[str, Any]
    raw_tool_response: Any
    formatted_response: str

class OrchestratorResponse(BaseModel):
    success: bool
    response: str
    intent: str
    topic: str
    emotional_state: str
    suggestions: List[str] = []

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
    elif "explanation" in intent or "explain" in intent:
        suggestions.extend([
            "Provide practice questions",
            "Create summarized notes",
            "Test understanding via flashcards"
        ])
    elif "note" in intent:
        suggestions.extend([
            "Create flashcards from notes",
            "Generate practice questions",
            "Get concept explanations"
        ])
    
    if emotion in ["confused", "anxious", "frustrated"]:
        suggestions.append("Break content into simpler parts")
    if emotion == "confident":
        suggestions.append("Try challenging problems")
    
    return suggestions[:3]
