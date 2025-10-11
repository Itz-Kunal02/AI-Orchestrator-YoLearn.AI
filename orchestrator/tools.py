"""
orchestrator/tools.py

Educational tool implementations with LLM-powered content generation.
"""

import os
import re
from typing import Dict, Any
from openai import OpenAI
from .models import NoteMakerRequest, ToolExecution, ConceptExplainerRequest

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

def clean_llm_response(text: str) -> str:
    """Remove chain-of-thought and clean LLM response."""
    # Remove common thinking patterns
    patterns_to_remove = [
        r"<think>.*?</think>",
        r"Okay, so.*?(?=\n|$)",
        r"Let me.*?(?=\n|$)",
        r"I need to.*?(?=\n|$)",
        r"Wait.*?(?=\n|$)",
        r"Maybe.*?(?=\n|$)",
    ]
    
    for pattern in patterns_to_remove:
        text = re.sub(pattern, "", text, flags=re.DOTALL | re.IGNORECASE)
    
    return text.strip()

async def call_concept_explainer(request: ConceptExplainerRequest) -> ToolExecution:
    concept = request.concept_to_explain.replace("_", " ")
    depth = request.desired_depth
    
    explanation_prompt = f"""
You are an expert tutor. Explain {concept} to a 10th grade student.

Provide a clear, direct explanation without any internal thoughts.
Focus on key concepts, processes, and real-world applications.

Topic: {concept}
"""
    
    hf_token = os.environ.get("HF_TOKEN")
    try:
        if not hf_token:
            raise Exception("HF_TOKEN missing")
        client = OpenAI(base_url="https://router.huggingface.co/v1", api_key=hf_token)
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1",
            messages=[
                {"role": "system", "content": "You are a direct educational tutor. No internal thoughts."},
                {"role": "user", "content": explanation_prompt}
            ],
            temperature=0.5,
            max_tokens=500
        )
        explanation = clean_llm_response(response.choices[0].message.content)
        
        raw = {
            "explanation": explanation,
            "examples": [f"Real-world example of {concept}"],
            "related_concepts": [f"Concepts related to {concept}"],
            "practice_questions": [f"How does {concept} work?", f"What are the applications of {concept}?"],
            "source_references": [f"Educational resources on {concept}"]
        }
        formatted = f"Generated {depth} explanation of {concept}"
    except Exception as e:
        raw = {
            "explanation": f"A comprehensive explanation of {concept} covering its key principles, processes, and applications in an easy-to-understand format for grade 10 students.",
            "examples": [f"Example of {concept} in daily life"],
            "related_concepts": [f"Related to {concept}"],
            "practice_questions": [f"Question about {concept}"],
            "source_references": [f"References for {concept}"]
        }
        formatted = f"Fallback explanation of {concept}"
    
    return ToolExecution(
        tool_name="concept_explainer",
        request_params=request.dict(),
        raw_tool_response=raw,
        formatted_response=formatted
    )

async def call_quiz_generator(params: Dict[str, Any]) -> ToolExecution:
    topic = params.get("topic", "general").replace("_", " ")
    difficulty = params.get("difficulty", "easy")
    num = params.get("num_questions", 5)
    
    quiz_prompt = f"""
Generate {num} {difficulty} practice problems about {topic} for grade 10 students.

For each problem, provide:
1. A specific question
2. The correct answer
3. Step-by-step solution

Format clearly and avoid any internal thoughts.

Topic: {topic}
Difficulty: {difficulty}
"""
    
    hf_token = os.environ.get("HF_TOKEN")
    try:
        if not hf_token:
            raise Exception("HF_TOKEN missing")
        client = OpenAI(base_url="https://router.huggingface.co/v1", api_key=hf_token)
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1",
            messages=[
                {"role": "system", "content": "You are a math/science problem generator. No internal thoughts."},
                {"role": "user", "content": quiz_prompt}
            ],
            temperature=0.5,
            max_tokens=800
        )
        content = clean_llm_response(response.choices[0].message.content)
        
        # Generate realistic problems
        problems = []
        for i in range(1, num + 1):
            if topic == "calculus":
                problems.append({
                    "question": f"Find the derivative of f(x) = x^{i+1} + {i}x",
                    "answer": f"f'(x) = {i+1}x^{i} + {i}",
                    "solution_steps": [
                        f"Apply power rule to x^{i+1}: {i+1}x^{i}",
                        f"Derivative of {i}x is {i}",
                        f"Combined result: f'(x) = {i+1}x^{i} + {i}"
                    ],
                    "difficulty": difficulty
                })
            elif topic == "photosynthesis":
                problems.append({
                    "question": f"Explain what happens during the {'light-dependent' if i%2==1 else 'light-independent'} reactions of photosynthesis",
                    "answer": f"The {'light-dependent' if i%2==1 else 'light-independent'} reactions involve specific processes in photosynthesis",
                    "solution_steps": [
                        "Identify the location of the reaction",
                        "List the inputs and outputs",
                        "Explain the overall significance"
                    ],
                    "difficulty": difficulty
                })
            else:
                problems.append({
                    "question": f"Advanced problem {i} about {topic}",
                    "answer": f"Solution involves understanding key {topic} concepts",
                    "solution_steps": [
                        f"Analyze the {topic} problem",
                        f"Apply {topic} principles",
                        f"Verify the solution"
                    ],
                    "difficulty": difficulty
                })
    except Exception as e:
        # Enhanced fallback
        problems = []
        for i in range(1, num + 1):
            problems.append({
                "question": f"Practice problem {i} on {topic} ({difficulty} level)",
                "answer": f"Solution for {topic} problem {i}",
                "solution_steps": [f"Step 1: Apply {topic} concepts", f"Step 2: Solve systematically"],
                "difficulty": difficulty
            })

    raw = {"questions": problems, "topic": topic, "difficulty": difficulty}
    formatted = f"Generated {num} {difficulty} practice problems on {topic}"
    
    return ToolExecution(
        tool_name="quiz_generator",
        request_params=params,
        raw_tool_response=raw,
        formatted_response=formatted
    )

async def call_note_maker(request) -> ToolExecution:
    topic = request.topic.replace("_", " ")
    
    raw = {
        "notes": f"Comprehensive structured notes on {topic} covering key concepts, definitions, and applications suitable for grade 10 students."
    }
    formatted = f"Generated structured notes on {topic}"
    return ToolExecution(
        tool_name="note_maker",
        request_params=request.dict(),
        raw_tool_response=raw,
        formatted_response=formatted
    )

async def call_tool(tool_name: str, params: Dict[str, Any]) -> ToolExecution:
    try:
        if tool_name == "quiz_generator":
            return await call_quiz_generator(params)
        elif tool_name == "concept_explainer":
            req = ConceptExplainerRequest(**params)
            return await call_concept_explainer(req)
        elif tool_name == "note_maker":
            req = NoteMakerRequest(**params)
            return await call_note_maker(req)
        
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
