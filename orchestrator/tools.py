"""
orchestrator/tools.py

Educational tool implementations and routing for YoLearn.ai Orchestrator.
Includes quiz_generator, flashcard_generator, note_maker, and concept_explainer.
"""

import random
from typing import Dict, Any
from urllib import response
from .models import (
    ToolExecution,
    FlashcardGeneratorRequest,
    NoteMakerRequest,
    ConceptExplainerRequest,
)

def pick_tool_from_intent(intent: str) -> str:
    """Select the appropriate educational tool based on the extracted intent."""
    i = intent.lower()
    if i == "request_practice_problems":
        return "quiz_generator"
    if i == "explanation":
        return "concept_explainer"
    if i == "notes":
        return "note_maker"
    return "quiz_generator"

async def call_quiz_generator(params: Dict[str, Any]) -> ToolExecution:
    """Generate practice problems (quiz_generator)."""
    topic = params.get("topic", "general").replace("_", " ")
    difficulty = params.get("difficulty", "easy")
    num = params.get("num_questions", 5)

    problems = []
    for i in range(1, num + 1):
        if "calculus" in topic:
            q = f"Compute the derivative of f(x) = x^{i+1}"
            a = f"{i+1}*x^{i}"
        else:
            q = f"Practice problem {i} on {topic}"
            a = f"Solution for problem {i}"
        problems.append({
            "question": q,
            "answer": a,
            "solution_steps": ["Step 1: apply rule...", "Step 2: simplify..."],
            "difficulty": difficulty
        })

    raw = {"questions": problems, "topic": params.get("topic"), "difficulty": difficulty}
    formatted = f"Generated {num} {difficulty} practice problems on {params.get('topic')}"

    return ToolExecution(
        tool_name="quiz_generator",
        request_params=params,
        raw_tool_response=raw,
        formatted_response=formatted
    )

async def call_flashcard_generator(request: FlashcardGeneratorRequest) -> ToolExecution:
    """Generate flashcards (flashcard_generator)."""
    # ... existing flashcard logic producing 'response' ...
    raw = response.dict()
    formatted = f"Created {len(response.flashcards)} {response.difficulty} flashcards on {response.topic}"
    return ToolExecution(
        tool_name="flashcard_generator",
        request_params=request.dict(),
        raw_tool_response=raw,
        formatted_response=formatted
    )

async def call_note_maker(request: NoteMakerRequest) -> ToolExecution:
    """Generate structured notes (note_maker)."""
    # ... existing note-making logic producing 'response' ...
    raw = response.dict()
    formatted = f"Generated structured notes on {response.topic}"
    return ToolExecution(
        tool_name="note_maker",
        request_params=request.dict(),
        raw_tool_response=raw,
        formatted_response=formatted
    )

async def call_concept_explainer(request: ConceptExplainerRequest) -> ToolExecution:
    """Generate concept explanations (concept_explainer)."""
    concept = request.concept_to_explain.replace("_", " ")
    depth = request.desired_depth

    # Example explanation generation
    explanation = f"This is a {depth} explanation of {concept}."
    raw = {
        "explanation": explanation,
        "examples": [f"Example of {concept}"],
        "related_concepts": [f"Related concept 1"],
        "practice_questions": [f"Practice question about {concept}"],
        "source_references": [f"Reference for {concept}"]
    }
    formatted = f"Generated {depth} explanation of {concept}"

    return ToolExecution(
        tool_name="concept_explainer",
        request_params=request.dict(),
        raw_tool_response=raw,
        formatted_response=formatted
    )

async def call_tool(tool_name: str, params: Dict[str, Any]) -> ToolExecution:
    """Route to the correct tool execution function."""
    try:
        if tool_name == "quiz_generator":
            return await call_quiz_generator(params)

        if tool_name == "flashcard_generator":
            req = FlashcardGeneratorRequest(**params)
            return await call_flashcard_generator(req)

        if tool_name == "note_maker":
            req = NoteMakerRequest(**params)
            return await call_note_maker(req)

        if tool_name == "concept_explainer":
            req = ConceptExplainerRequest(**params)
            return await call_concept_explainer(req)

        # Fallback for unsupported tools
        raw = {"message": "Tool not supported yet"}
        return ToolExecution(
            tool_name=tool_name,
            request_params=params,
            raw_tool_response=raw,
            formatted_response="Generated fallback response"
        )

    except Exception as e:
        return ToolExecution(
            tool_name=tool_name,
            request_params=params,
            raw_tool_response={"error": str(e)},
            formatted_response=f"Error generating content for {params.get('topic','')}"
        )
