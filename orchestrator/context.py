# orchestrator/context.py

"""
Robust context extraction with preprocessing for spelling correction and verb stripping.
Uses DeepSeek-R1 or falls back gracefully.
"""

import os
import re
import json
from typing import Dict
from openai import OpenAI

# Simple common misspelling corrections dictionary
MISSPELLINGS = {
    "expalin": "explain",
    "dificult": "difficult",
    "quize": "quiz",
    "praktice": "practice",
    # add more as needed
}

# Verbs to strip from topic after intent extraction
VERBS_TO_REMOVE_FROM_TOPIC = [
    "explain",
    "describe",
    "tell",
    "show",
    "give",
    "please",
    "can you",
    "could you",
    "would you",
    "i want",
    "i need",
    "help with",
]

def preprocess_input(user_input: str) -> str:
    text = user_input.lower()
    
    # Correct common misspellings
    for wrong, right in MISSPELLINGS.items():
        text = re.sub(rf"\b{re.escape(wrong)}\b", right, text)
    
    return text

def strip_verbs(topic: str) -> str:
    original = topic
    for verb in VERBS_TO_REMOVE_FROM_TOPIC:
        pattern = rf"^{re.escape(verb)}\s*"
        topic = re.sub(pattern, "", topic)
    return topic.strip()

def extract_context(user_input: str) -> Dict[str, str]:
    """Extract context with LLM and robust fallback."""
    clean_input = preprocess_input(user_input)

    prompt = (
        "You are an educational AI assistant. "
        "Extract and return a JSON object with keys: intent, topic, emotional_state. "
        "Ensure 'topic' is the main subject (multi-word topics using underscores). "
        "Respond ONLY with valid JSON."
    )

    hf_token = os.environ.get("HF_TOKEN")
    if hf_token:
        try:
            client = OpenAI(base_url="https://router.huggingface.co/v1", api_key=hf_token)
            completion = client.chat.completions.create(
                model="deepseek-ai/DeepSeek-R1",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": clean_input}
                ],
                temperature=0.7,
                max_tokens=150
            )
            resp = completion.choices[0].message.content.strip()
            match = re.search(r"\{.*\}", resp, flags=re.DOTALL)
            if match:
                context = json.loads(match.group())
                # Validate presence of keys and their types
                for key in ("intent", "topic", "emotional_state"):
                    if key not in context or not isinstance(context[key], str):
                        raise ValueError(f"Missing or invalid key '{key}' in LLM response")
                # Clean topic
                context["topic"] = strip_verbs(context["topic"].replace(" ", "_"))
                return context

        except Exception:
            pass  # Fall through to fallback

    # Fallback
    ui = clean_input

    # Intent
    if any(w in ui for w in ["practice", "problem", "quiz", "exercise"]):
        intent = "request_practice_problems"
    elif any(w in ui for w in ["explain", "detail", "teach", "describe"]):
        intent = "explanation"
    elif any(w in ui for w in ["note", "summary", "summarize"]):
        intent = "notes"
    else:
        intent = "request_practice_problems"

    # Topic extraction after removing verbs
    topic_candidate = ui
    for verb in VERBS_TO_REMOVE_FROM_TOPIC:
        pattern = f"{verb}\\s*"
        topic_candidate = re.sub(pattern, "", topic_candidate)
    topic_candidate = topic_candidate.strip()

    # Use first two words (if any) or 'general'
    words = topic_candidate.split()
    topic = "_".join(words[:2]) if words else "general"

    emotional_state = "neutral"
    if any(w in ui for w in ["struggl", "frustrat", "confus", "hard"]):
        emotional_state = "frustrated"
    elif any(w in ui for w in ["confident", "know", "understand"]):
        emotional_state = "confident"

    return {
        "intent": intent,
        "topic": topic,
        "emotional_state": emotional_state
    }
