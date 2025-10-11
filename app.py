import os
import asyncio
import json
import nest_asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from dotenv import load_dotenv

# Load environment variables from .env (HF_TOKEN, etc.)
load_dotenv()

# Import all modules
from orchestrator.models import (
    OrchestratorRequest,
    FullOrchestratorResponse,
    generate_suggestions,
)
from orchestrator.context import extract_context
from orchestrator.tools import call_tool
from orchestrator.params import extract_tool_params
from orchestrator.session import init_session, _default_user, SESSIONS

# Apply nest_asyncio for compatibility (needed for TestClient + asyncio)
nest_asyncio.apply()

# Create FastAPI app
app = FastAPI(title="YoLearn AI Orchestrator", version="1.0")


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "model": "deepseek-ai/DeepSeek-R1"}


@app.post("/api/orchestrate_full", response_model=FullOrchestratorResponse)
async def orchestrate_full(req: OrchestratorRequest):
    """Main orchestration endpoint"""
    # Step 1: Set up session tracking
    session_id = init_session(req.user_id, req.session_id)

    # Step 2: Extract context using AI (or robust fallback)
    ctx = extract_context(req.user_input)
    intent, topic, emotion = ctx["intent"], ctx["topic"], ctx["emotional_state"]

    # Step 3: Get user profile and history
    user_profile = _default_user()
    chat_history = SESSIONS[session_id]["history"]

    # Step 4: Extract tool parameters (emotion-aware)
    tool_name, tool_params = extract_tool_params(
        intent, topic, emotion, user_profile, chat_history
    )

    # Step 5: Execute tool
    execution = await call_tool(tool_name, tool_params)

    # Step 6: Generate suggestions
    suggestions = generate_suggestions(intent, emotion)

    # Optional: Append to session history (basic)
    chat_history.append({"role": "user", "message": req.user_input})
    chat_history.append({"role": "assistant", "message": execution.formatted_response})

    # Step 7: Return full response
    return FullOrchestratorResponse(
        success=True,
        response=execution.formatted_response,
        intent=intent,
        topic=topic,
        emotional_state=emotion,
        suggestions=suggestions,
        tool_execution=execution,
        session_id=session_id,
        next_actions=["Review flashcards", "Request notes", "Get explanation"],
    )


# -------------------------
# Demo runner + Chat runner
# -------------------------
def _print_full_json(obj):
    print(json.dumps(obj, indent=2, ensure_ascii=False))


async def run_demo_tests():
    """Run the predefined demo tests and print FULL JSON like your desired output."""
    print("🎓 YoLearn.ai Orchestrator Demo")
    print("=" * 50)

    tc = TestClient(app)

    test_cases = [
        {
            "input": "I'm struggling with calculus derivatives and need practice problems",
            "user_id": "student123",
            "description": "Frustrated student needing practice",
        },
        {
            "input": "give detailed explanation",
            "user_id": "student123",
            "description": "Request for explanation",
        },
        {
            "input": "I understand photosynthesis well, give me advanced content",
            "user_id": "student456",
            "description": "Confident student seeking challenge",
        },
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: {test_case['description']}")
        print(f"📝 Input: {test_case['input']}")
        print("-" * 50)

        payload = {"user_input": test_case["input"], "user_id": test_case["user_id"]}
        resp = tc.post("/api/orchestrate_full", json=payload)
        _print_full_json(resp.json())
        print("=" * 50)


async def chat_loop():
    """
    Interactive chat mode that prints FULL JSON per turn.
    Type 'exit' to quit.
    """
    print("Enter your user_id (default: student_demo): ", end="")
    user_id = input().strip() or "student_demo"
    session_id = None
    print("YoLearn.ai Chat - type 'exit' to quit.")

    while True:
        print("\nYou: ", end="")
        user_input = input().strip()
        if not user_input or user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        req = OrchestratorRequest(user_input=user_input, user_id=user_id, session_id=session_id)
        resp: FullOrchestratorResponse = await orchestrate_full(req)

        # Print FULL JSON response (not a short sentence)
        _print_full_json(resp.model_dump())

        # Keep session for continuity
        session_id = resp.session_id


if __name__ == "__main__":
    # Choose mode by ENV flag: DEMO_MODE=1 runs predefined tests, else run interactive chat
    DEMO_MODE = os.environ.get("DEMO_MODE", "0") == "1"

    # Ensure HF_TOKEN is visible (for debugging). Do not hardcode; rely on .env
    if not os.environ.get("HF_TOKEN"):
        print("⚠️  HF_TOKEN not found in environment; AI calls will use fallback extraction.")

    if DEMO_MODE:
        asyncio.run(run_demo_tests())
    else:
        asyncio.run(chat_loop())
