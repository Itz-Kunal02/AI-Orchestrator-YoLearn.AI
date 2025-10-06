# API Documentation

## Base URL
http://localhost:8000

## Endpoints

### Health Check
GET /health

text

**Response:**
{
"status": "healthy",
"model": "deepseek-ai/DeepSeek-R1"
}

text

### Main Orchestration
POST /api/orchestrate_full

text

**Request:**
{
"user_input": "I'm struggling with calculus derivatives and need practice problems",
"user_id": "student123",
"session_id": "optional"
}

**Response:**
{
"success": true,
"response": "Generated 5 easy questions on calculus_derivatives",
"intent": "request_practice_problems",
"topic": "calculus_derivatives",
"emotional_state": "frustrated",
"suggestions": [...],
"tool_execution": {...},
"session_id": "student123_1234567890",
"next_actions": [...]
}

