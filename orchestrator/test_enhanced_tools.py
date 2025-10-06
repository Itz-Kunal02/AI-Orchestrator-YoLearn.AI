"""Test enhanced tool integration"""

import asyncio
from fastapi.testclient import TestClient
from app import app

def test_enhanced_orchestration():
    """Test the enhanced tool integration"""
    tc = TestClient(app)
    
    # Test scenarios
    test_cases = [
        {
            "input": "I need organized notes about calculus derivatives",
            "expected_tool": "note_maker",
            "description": "Should trigger note maker with structured format"
        },
        {
            "input": "Create flashcards to help me memorize photosynthesis steps", 
            "expected_tool": "flashcard_generator",
            "description": "Should trigger flashcard generator"
        },
        {
            "input": "Please explain quantum mechanics to me step by step",
            "expected_tool": "concept_explainer", 
            "description": "Should trigger concept explainer"
        },
        {
            "input": "I'm frustrated with calculus derivatives and need practice problems",
            "expected_tool": "flashcard_generator",
            "description": "Should trigger flashcard with easy difficulty due to frustration"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: {test_case['description']}")
        print(f"📝 Input: {test_case['input']}")
        
        payload = {
            "user_input": test_case["input"],
            "user_id": f"test_student_{i}"
        }
        
        response = tc.post("/api/orchestrate_full", json=payload)
        result = response.json()
        
        if result["success"]:
            print(f"✅ Tool Selected: {result['tool_execution']['tool_name']}")
            print(f"📊 Response: {result['response']}")
            print(f"🎯 Intent: {result['intent']}")
            print(f"💭 Emotion: {result['emotional_state']}")
            print(f"💡 Suggestions: {result['suggestions']}")
        else:
            print(f"❌ Failed: {result}")

if __name__ == "__main__":
    test_enhanced_orchestration()
