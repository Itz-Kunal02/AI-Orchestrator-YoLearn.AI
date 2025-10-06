import os
import nest_asyncio
import asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Import all modules
from orchestrator.models import (
    OrchestratorRequest, 
    FullOrchestratorResponse, 
    generate_suggestions
)
from orchestrator.context import extract_context
from orchestrator.tools import call_tool
from orchestrator.params import extract_tool_params
from orchestrator.session import init_session, _default_user, SESSIONS

# Apply nest_asyncio for compatibility
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
    
    # Step 2: Extract context using AI
    ctx = extract_context(req.user_input)
    intent, topic, emotion = ctx["intent"], ctx["topic"], ctx["emotional_state"]
    
    # Step 3: Get user profile and history
    user_profile = _default_user()
    chat_history = SESSIONS[session_id]["history"]
    
    # Step 4: Extract tool parameters
    tool_name, tool_params = extract_tool_params(intent, topic, emotion, user_profile, chat_history)
    
    # Step 5: Execute tool
    execution = await call_tool(tool_name, tool_params)
    
    # Step 6: Generate suggestions
    suggestions = generate_suggestions(intent, emotion)
    
    # Step 7: Return response
    return FullOrchestratorResponse(
        success=True,
        response=execution.formatted_response,
        intent=intent,
        topic=topic,
        emotional_state=emotion,
        suggestions=suggestions,
        tool_execution=execution,
        session_id=session_id,
        next_actions=["Review flashcards", "Request notes", "Get explanation"]
    )


if __name__ == "__main__":
    """
    Interactive chat mode: allows typing student inputs directly
    """
    async def chat_loop():
        user_id = input("Enter your user_id: ").strip() or "student_demo"
        session_id = None
        print("YoLearn.ai Chat - type 'exit' to quit.")
        while True:
            user_input = input("\nYou: ").strip()
            if not user_input or user_input.lower() in ("exit", "quit"):
                print("Goodbye!")
                break

            # Build request model
            req = OrchestratorRequest(
                user_input=user_input,
                user_id=user_id,
                session_id=session_id
            )
            # Call orchestrator
            resp: FullOrchestratorResponse = await orchestrate_full(req)
            # Print formatted response
            print(f"\nAI Tutor: {resp.response}")
            # Print suggestions
            print("Suggestions:", ", ".join(resp.suggestions))
            # Update session_id
            session_id = resp.session_id

    # Run the async chat loop
    asyncio.run(chat_loop())
