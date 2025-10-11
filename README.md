# AI Orchestrator – YoLearn.ai
Intelligent Multi-Tool Orchestration for an Autonomous AI Tutoring System

***

## Overview
An intelligent, multi-tool orchestration system that transforms natural student conversations into the right educational actions using DeepSeek-R1. Built for scale, cost-efficiency, and personalization, this system autonomously selects tools, extracts parameters, and returns adaptive learning content.

***

## Features
- Context-aware intent, topic, and emotion extraction powered by DeepSeek-R1
- Multi-tool orchestration with schema-driven parameter mapping
- Adaptive difficulty based on emotional state (frustrated → easy, confident → hard)
- Session management for conversation continuity
- Production-ready FastAPI endpoints with TestClient-based testing
- Extensible architecture designed for 80+ tools integration

***

## Architecture
- Context Analysis → Tool Selection → Parameter Extraction → Tool Execution → Response Formatting
- Modular components:
  - Context Analyzer (DeepSeek-R1 with robust fallback)
  - Tool Selector (intent-driven mapping)
  - Parameter Extractor (schema + inference)
  - Tool Runner (mock/real integration)
  - Session Manager (in-memory; DB-ready)
  - Adaptive Responder (suggestions + next actions)

***

## Quick Start
1. Clone the repository:
   ```
   git clone https://github.com/Kunal02/yolearn-ai-orchestrator.git
   cd yolearn-ai-orchestrator
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set Hugging Face token:
   ```
   export HF_TOKEN="YOUR_HF_TOKEN"
   # Windows PowerShell: $env:HF_TOKEN="YOUR_HF_TOKEN"
   # Windows CMD: set HF_TOKEN=YOUR_HF_TOKEN
   ```

5. Run locally:
   ```
   uvicorn app:app --reload
   ```

6. Test endpoint with curl:
   ```
   curl -X POST http://127.0.0.1:8000/api/orchestrate_full \
     -H "Content-Type: application/json" \
     -d '{"user_input":"I am struggling with calculus derivatives and need practice problems","user_id":"student123"}'
   ```

***

## API

### Health
- GET /health  
- Response:
  ```
  {"status":"healthy","model":"deepseek-ai/DeepSeek-R1"}
  ```

### Orchestrate (Full)
- POST /api/orchestrate_full  
- Request:
  ```
  {
    "user_input": "I'm struggling with calculus derivatives and need practice problems",
    "user_id": "student123",
    "session_id": "optional"
  }
  ```
- Response (example):
  ```
  {
    "success": true,
    "response": "Generated 5 easy questions on calculus_derivatives",
    "intent": "request_practice_problems",
    "topic": "calculus_derivatives",
    "emotional_state": "frustrated",
    "suggestions": [
      "Generate flashcards for practice",
      "Provide concise notes summary",
      "Ask for detailed concept explanation"
    ],
    "tool_execution": {
      "tool_name": "quiz_generator",
      "request_params": {
        "difficulty": "easy",
        "question_type": "practice",
        "num_questions": 5,
        "topic": "calculus_derivatives",
        "subject": "calculus_derivatives"
      },
      "raw_tool_response": "Generated 5 easy questions on calculus_derivatives",
      "formatted_response": "Generated 5 easy questions on calculus_derivatives"
    },
    "session_id": "student123",
    "next_actions": [
      "Review flashcards",
      "Request notes",
      "Get explanation"
    ]
  }
  ```

***

## Configuration
Environment variables:
- HF_TOKEN: Hugging Face API token for DeepSeek-R1 via HF Inference Router

Dependency highlights:
- FastAPI for API
- Pydantic for validation
- OpenAI SDK (pointed to HF router) for DeepSeek-R1
- TestClient for inline tests

***

## Development
- Rapid prototyping was done in Google Colab to iterate quickly.
- Code is modular and well-commented for maintainability and collaboration.
- For live demo and production, the code will be demonstrated in a VS Code environment if shortlisted.

Suggested folder structure:
```
.
├── app.py                 # FastAPI application
├── orchestrator/          # Core modules (context, tools, params, session)
├── tests/                 # API and unit tests
├── requirements.txt
├── README.md
└── docs/
    ├── architecture.md
    ├── api.md
    └── demo-guide.md
```

***

## Roadmap
- Real educational tool APIs (Quiz, Notes, Explainer, Flashcards)
- Database-backed sessions and student profiles
- Spaced repetition scheduling and curriculum alignment
- Analytics dashboard for learning insights
- Multimodal support (speech, images)
- Dynamic schema onboarding for 80+ tools

***

## Contributing
Contributions are welcome:
- Fork the repo
- Create a feature branch
- Add tests and documentation
- Open a pull request


***

## Acknowledgments
- DeepSeek-R1 via Hugging Face Router for world-class reasoning
- FastAPI & Pydantic for a clean, scalable service layer
- The YoLearn.ai community for driving innovation in education

***

