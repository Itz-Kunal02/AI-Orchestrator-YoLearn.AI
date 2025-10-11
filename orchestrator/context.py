# orchestrator/context.py

import os
import json
import re
from typing import Dict
from openai import OpenAI

def extract_last_json(text: str) -> Dict[str, str]:
    """Extract the last valid JSON object from text."""
    patterns = [
        r'\{[^{}]*"intent"[^{}]*"topic"[^{}]*"emotional_state"[^{}]*\}',
        r'\{[^{}]*"intent"[^{}]*\}',
        r'\{.*?"intent".*?\}',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.DOTALL)
        for match in reversed(matches):
            try:
                parsed = json.loads(match)
                if all(k in parsed for k in ("intent", "topic", "emotional_state")):
                    return parsed
            except:
                continue
    
    raise ValueError("No valid JSON found")

def manual_extraction(user_input: str) -> Dict[str, str]:
    """Manual extraction as final fallback when LLM fails."""
    ui = user_input.lower()
    
    # Determine intent
    if any(word in ui for word in ["practice", "problems", "quiz", "test", "exercise", "advanced problems"]):
        intent = "request_practice_problems"
    elif any(word in ui for word in ["notes", "summary", "summarize"]):
        intent = "notes"
    else:
        intent = "explanation"
    
    # Enhanced topic detection
    topic = "general"
    topics = {
        "calculus": ["calculus", "derivative", "derivatives", "integral", "limit"],
        "photosynthesis": ["photosynthesis", "photosyn"],
        "quantum_mechanics": ["quantum", "quantum mechanics", "mechanics"],
        "biology": ["biology", "bio"],
        "chemistry": ["chemistry", "chem"],
        "physics": ["physics", "phys"],
        "math": ["math", "mathematics"],
        "algebra": ["algebra"],
        "geometry": ["geometry"],
    }
    
    for topic_name, keywords in topics.items():
        if any(keyword in ui for keyword in keywords):
            topic = topic_name
            break
    
    # Determine emotional state
    emotional_state = "neutral"
    if any(word in ui for word in ["struggling", "confused", "hard", "difficult", "help"]):
        emotional_state = "frustrated"
    elif any(word in ui for word in ["confident", "easy", "understand", "know", "well"]):
        emotional_state = "confident"
    
    return {"intent": intent, "topic": topic, "emotional_state": emotional_state}

def extract_context(user_input: str) -> Dict[str, str]:
    """Extract context with LLM first, then manual fallback."""
    hf_token = os.environ.get("HF_TOKEN")
    
    if hf_token:
        try:
            client = OpenAI(base_url="https://router.huggingface.co/v1", api_key=hf_token)
            
            simple_prompt = f"""
Extract from: "{user_input}"

Return only this JSON format:
{{"intent":"explanation","topic":"calculus","emotional_state":"neutral"}}

Intent options: explanation, notes, request_practice_problems
Topic: main subject (fix spelling)
Emotional state: neutral, frustrated, confident, anxious
"""
            
            response = client.chat.completions.create(
                model="deepseek-ai/DeepSeek-R1",
                messages=[
                    {"role": "system", "content": "Output only JSON. No other text."},
                    {"role": "user", "content": simple_prompt}
                ],
                temperature=0,
                max_tokens=100,
            )
            
            resp_text = response.choices[0].message.content.strip()
            context = extract_last_json(resp_text)
            print(f"DEBUG: LLM extracted: {context}")
            return context
            
        except Exception as e:
            print(f"LLM extraction failed: {e}")
    
    # Manual extraction fallback
    context = manual_extraction(user_input)
    print(f"DEBUG: Manual extracted: {context}")
    return context
