# YoLearn AI Orchestrator API

An intelligent educational AI system that provides personalized learning content, practice problems, and explanations based on student input and emotional state.

![API Status](https://img.shields.io/badge/status-production--ready-green)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-teal)

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- HuggingFace API Token (optional, for full AI functionality)
- FastAPI dependencies (see `requirements.txt`)

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/yolearn-ai-orchestrator.git
cd yolearn-ai-orchestrator
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**:
```bash
# Create .env file
echo "HF_TOKEN=your_huggingface_token_here" > .env
```

4. **Run the server**:
```bash
# Method 1: Using uvicorn (recommended)
uvicorn app:app --host 0.0.0.0 --port 8000 --reload

# Method 2: Direct Python execution
python app.py
```

5. **Verify installation**:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "model": "deepseek-ai/DeepSeek-R1"
}
```

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🛠 API Endpoints

### 1. Health Check
**GET** `/health`

Check API status and model availability.

**Response**:
```json
{
  "status": "healthy",
  "model": "deepseek-ai/DeepSeek-R1",
  "hf_token": "available"
}
```

### 2. Main Orchestration
**POST** `/api/orchestrate_full`

Main endpoint for educational AI interactions.

**Request Body**:
```json
{
  "user_input": "I'm struggling with calculus derivatives and need practice problems",
  "user_id": "student123",
  "session_id": "optional_session_id"
}
```

**Response**:
```json
{
  "success": true,
  "response": "Generated 5 easy practice problems on calculus",
  "intent": "request_practice_problems",
  "topic": "calculus",
  "emotional_state": "frustrated",
  "suggestions": [
    "Generate flashcards for practice",
    "Provide concise notes summary",
    "Ask for detailed concept explanation"
  ],
  "tool_execution": {
    "tool_name": "quiz_generator",
    "request_params": {...},
    "raw_tool_response": {...},
    "formatted_response": "Generated 5 easy practice problems on calculus"
  },
  "session_id": "student123_1760247391",
  "next_actions": [
    "Review flashcards",
    "Request notes",
    "Get explanation"
  ]
}
```

### 3. Session Management
**GET** `/api/sessions/{user_id}`

Get all sessions for a specific user.

**DELETE** `/api/sessions/{session_id}`

Clear a specific session.

## 🎯 System Capabilities

### Intent Detection
The system automatically detects three types of learning intents:

1. **`explanation`** - When students ask for explanations
   - *Example*: "Explain photosynthesis step by step"
   - *Tool*: `concept_explainer`

2. **`notes`** - When students request summaries or notes  
   - *Example*: "Give me notes on quantum mechanics"
   - *Tool*: `note_maker`

3. **`request_practice_problems`** - When students need practice
   - *Example*: "I need calculus derivative problems"
   - *Tool*: `quiz_generator`

### Topic Extraction
Supports any educational topic with automatic spelling correction:
- Mathematics: calculus, algebra, geometry
- Sciences: physics, chemistry, biology, photosynthesis
- Advanced: quantum mechanics, machine learning
- And more...

### Emotional State Recognition
Detects student emotional state for personalized responses:
- **`frustrated`** - "struggling", "confused", "hard"
- **`confident`** - "understand well", "easy", "advanced"
- **`neutral`** - Default state
- **`anxious`** - "worried", "nervous"

## 💻 Frontend Integration

### JavaScript/React Example

```javascript
// API client function
async function callYoLearnAPI(userInput, userId, sessionId = null) {
  const response = await fetch('http://localhost:8000/api/orchestrate_full', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      user_input: userInput,
      user_id: userId,
      session_id: sessionId
    })
  });
  
  return await response.json();
}

// React component example
import React, { useState } from 'react';

function AITutor() {
  const [input, setInput] = useState('');
  const [response, setResponse] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const result = await callYoLearnAPI(input, 'student123', sessionId);
      setResponse(result);
      setSessionId(result.session_id);
      setInput('');
    } catch (error) {
      console.error('API call failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="ai-tutor">
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask me anything about your studies..."
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Thinking...' : 'Ask AI Tutor'}
        </button>
      </form>

      {response && (
        <div className="response">
          <h3>AI Response:</h3>
          <p><strong>Intent:</strong> {response.intent}</p>
          <p><strong>Topic:</strong> {response.topic}</p>
          <p><strong>Mood:</strong> {response.emotional_state}</p>
          
          <div className="content">
            <h4>Response:</h4>
            <p>{response.response}</p>
          </div>

          <div className="suggestions">
            <h4>Suggestions:</h4>
            <ul>
              {response.suggestions.map((suggestion, index) => (
                <li key={index}>{suggestion}</li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}

export default AITutor;
```

### Python Client Example

```python
import requests

class YoLearnClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session_id = None
    
    def health_check(self):
        """Check API health"""
        response = requests.get(f"{self.base_url}/health")
        return response.json()
    
    def ask_tutor(self, user_input, user_id):
        """Main AI tutor interaction"""
        payload = {
            "user_input": user_input,
            "user_id": user_id,
            "session_id": self.session_id
        }
        
        response = requests.post(
            f"{self.base_url}/api/orchestrate_full",
            json=payload
        )
        
        result = response.json()
        self.session_id = result.get("session_id")  # Keep session continuity
        return result

# Usage example
client = YoLearnClient()

# Check if API is running
print(client.health_check())

# Ask for help
response = client.ask_tutor(
    "I need help with calculus derivatives", 
    "student123"
)

print(f"Intent: {response['intent']}")
print(f"Topic: {response['topic']}")
print(f"Response: {response['response']}")
```

### Flutter/Mobile Example

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class YoLearnAPI {
  static const String baseUrl = 'http://localhost:8000';
  String? sessionId;
  
  Future<Map<String, dynamic>> askTutor({
    required String userInput,
    required String userId,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/api/orchestrate_full'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'user_input': userInput,
        'user_id': userId,
        'session_id': sessionId,
      }),
    );
    
    if (response.statusCode == 200) {
      final result = json.decode(response.body);
      sessionId = result['session_id']; // Maintain session
      return result;
    } else {
      throw Exception('Failed to get AI response');
    }
  }
}

// Usage in Flutter widget
class AITutorPage extends StatefulWidget {
  @override
  _AITutorPageState createState() => _AITutorPageState();
}

class _AITutorPageState extends State<AITutorPage> {
  final YoLearnAPI api = YoLearnAPI();
  final TextEditingController _controller = TextEditingController();
  Map<String, dynamic>? _response;
  bool _loading = false;

  Future<void> _askTutor() async {
    setState(() => _loading = true);
    
    try {
      final response = await api.askTutor(
        userInput: _controller.text,
        userId: 'student123',
      );
      
      setState(() {
        _response = response;
        _controller.clear();
      });
    } catch (e) {
      // Handle error
    } finally {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('YoLearn AI Tutor')),
      body: Column(
        children: [
          Padding(
            padding: EdgeInsets.all(16.0),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    decoration: InputDecoration(
                      hintText: 'Ask me anything...',
                      border: OutlineInputBorder(),
                    ),
                  ),
                ),
                SizedBox(width: 8),
                ElevatedButton(
                  onPressed: _loading ? null : _askTutor,
                  child: Text(_loading ? 'Thinking...' : 'Ask'),
                ),
              ],
            ),
          ),
          if (_response != null) 
            Expanded(
              child: Padding(
                padding: EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('Intent: ${_response!['intent']}'),
                    Text('Topic: ${_response!['topic']}'),
                    Text('Mood: ${_response!['emotional_state']}'),
                    SizedBox(height: 16),
                    Text('Response:', style: TextStyle(fontWeight: FontWeight.bold)),
                    Text(_response!['response']),
                  ],
                ),
              ),
            ),
        ],
      ),
    );
  }
}
```

## 🔧 Development Setup

### Environment Variables

Create a `.env` file in the root directory:

```env
# Required for full AI functionality
HF_TOKEN=your_huggingface_token_here

# Optional configuration
PORT=8000
ENVIRONMENT=development
LOG_LEVEL=info

# Run modes
RUN_MODE=server  # Options: server, chat, demo
DEMO_MODE=0      # Set to 1 for demo mode
```

### Running in Different Modes

```bash
# Production server mode (default)
python app.py

# Interactive chat mode
RUN_MODE=chat python app.py

# Demo mode with predefined tests
RUN_MODE=demo python app.py
```

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Build and run with Docker
docker build -t yolearn-api .
docker run -p 8000:8000 -e HF_TOKEN=your_token_here yolearn-api
```

## 📊 Example API Calls

### 1. Request Explanation
```bash
curl -X POST "http://localhost:8000/api/orchestrate_full" \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "Can you explain photosynthesis step by step?",
    "user_id": "student456"
  }'
```

### 2. Request Practice Problems
```bash
curl -X POST "http://localhost:8000/api/orchestrate_full" \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "I need advanced calculus derivative problems",
    "user_id": "student789"
  }'
```

### 3. Request Notes
```bash
curl -X POST "http://localhost:8000/api/orchestrate_full" \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "Give me detailed notes on quantum mechanics",
    "user_id": "student101"
  }'
```

## 🔍 Error Handling

The API includes comprehensive error handling:

### Common Error Responses

```json
{
  "detail": "Internal server error: <error_message>",
  "status_code": 500
}
```

### Fallback Behavior

- **LLM unavailable**: Uses manual extraction and fallback content
- **Invalid input**: Returns appropriate error messages
- **Session issues**: Creates new sessions automatically

## 📈 Performance & Scaling

### Async Architecture
- Built on FastAPI with async/await support
- Handles multiple concurrent requests efficiently
- Non-blocking AI model calls

### Session Management
- Automatic session creation and tracking
- Session-based conversation continuity
- Memory-efficient session storage

### Caching Strategy
- Context extraction results cached per session
- Tool parameter optimization
- Reduced redundant AI calls

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request


## 🆘 Support

- **Issues**: Open an issue on GitHub
- **Documentation**: Visit `/docs` endpoint when running locally
- **Community**: Join our Discord/Slack (add links)

---

## 🎯 Production Checklist

Before deploying to production:

- [ ] Set proper CORS origins in `app.py`
- [ ] Configure proper environment variables
- [ ] Set up proper logging and monitoring
- [ ] Configure rate limiting
- [ ] Set up SSL/HTTPS
- [ ] Configure database for session persistence (if needed)
- [ ] Set up health monitoring endpoints
- [ ] Configure backup and recovery procedures

