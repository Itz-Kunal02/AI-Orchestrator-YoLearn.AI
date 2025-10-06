import os
import re
from typing import Dict

from openai import OpenAI


def extract_context(user_input: str) -> Dict[str, str]:
    """Extract intent, topic, and emotional state from user input"""
    prompt = """Extract JSON with keys: intent, topic, emotional_state from student message. Respond ONLY in JSON."""
    
    try:
        hf_token = os.environ.get('HF_TOKEN')
        if not hf_token:
            raise ValueError("HF_TOKEN not set")
            
        client = OpenAI(base_url="https://router.huggingface.co/v1", api_key=hf_token)
        
        completion = client.chat.completions.create(
            model='deepseek-ai/DeepSeek-R1',
            messages=[
                {"role": "system", "content": prompt}, 
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=200
        )
        
        resp = completion.choices[0].message.content.strip()
        json_part = re.search(r"\{.*\}", resp, flags=re.DOTALL).group()
        return eval(json_part)
        
   # In orchestrator/context.py

    except Exception as e:
        # Remove this fallback:
        # return {"intent":"request_practice_problems","topic":"calculus_derivatives","emotional_state":"frustrated"}
        
        # Instead, raise to surface the issue
        raise RuntimeError(f"Context analysis failed: {e}")

