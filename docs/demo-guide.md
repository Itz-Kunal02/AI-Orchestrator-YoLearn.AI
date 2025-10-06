# Demo Guide

## Setup
1. Clone repository
2. Create virtual environment: `python -m venv .venv`
3. Activate: `.venv\Scripts\Activate.ps1` (Windows) or `source .venv/bin/activate` (Mac/Linux)
4. Install dependencies: `pip install -r requirements.txt`
5. Set HF_TOKEN environment variable
6. Run: `python app.py` for direct test or `uvicorn app:app --reload` for web server

## Test Scenarios

### Scenario 1: Frustrated Student
**Input:** "I'm struggling with calculus derivatives and need practice problems"
**Expected:** Easy difficulty, quiz generator tool, supportive suggestions

### Scenario 2: Confident Student  
**Input:** "I understand photosynthesis well, give me advanced problems"
**Expected:** Hard difficulty, challenging content

### Scenario 3: Explanation Request
**Input:** "Can you explain quantum mechanics step by step?"
**Expected:** Concept explainer tool, appropriate depth

## Verification
- Context extraction should identify intent, topic, emotion
- Tool selection should match request type
- Parameter extraction should adapt to emotional state
- Response should include suggestions and next actions
