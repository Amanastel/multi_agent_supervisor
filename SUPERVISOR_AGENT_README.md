# 🤖 Supervisor Agent Documentation

## Overview

The **Supervisor Agent** is an intelligent task router and orchestrator that automatically analyzes user requests and routes them to the most appropriate specialized agent. It provides a single entry point for all calendar and email operations while optimizing performance by using the most efficient agent for each task.

## 🏗️ Architecture

```
User Request → Supervisor Agent → Task Analysis → Agent Selection → Execution → Response
```

### Available Agents

1. **Calendar Agent** - Specialized for calendar operations
2. **Gmail Agent** - Specialized for email operations  
3. **Unified Agent** - Handles complex workflows involving both calendar and email

## 🎯 Intelligent Routing Logic

### Calendar Agent Selection
- **Keywords**: schedule, meeting, calendar, event, availability, reschedule, appointment
- **Use Cases**: 
  - "Schedule a meeting tomorrow at 2 PM"
  - "Check my availability for Friday"
  - "List my events for next week"

### Gmail Agent Selection
- **Keywords**: email, send, mail, gmail, reply, forward, message, inbox
- **Use Cases**:
  - "Send an email to john@example.com"
  - "Search for emails from alice@company.com"
  - "Reply to the latest email"

### Unified Agent Selection
- **Keywords**: and, then, also, additionally, follow up
- **Use Cases**:
  - "Schedule a meeting and send invitation"
  - "Check calendar and send summary to team"
  - "Reschedule meeting and notify attendees"

## 📡 API Endpoints

### Main Chat Endpoint
```http
POST /api/supervisor/chat
```

**Request Body:**
```json
{
  "prompt": "Schedule a meeting tomorrow at 2 PM",
  "user_id": "optional_user_id",
  "preferred_agent": "auto"
}
```

**Response:**
```json
{
  "response": "✅ Event successfully scheduled...",
  "success": true,
  "selected_agent": "calendar",
  "reasoning": "The request is specifically about scheduling a meeting.",
  "task_description": "Schedule a meeting for the user tomorrow at 2 PM.",
  "error": null
}
```

### Task Analysis Endpoint
```http
POST /api/supervisor/analyze
```

**Request Body:**
```json
{
  "prompt": "Send an email to amankumar.ak0012@gmail.com"
}
```

**Response:**
```json
{
  "success": true,
  "analysis": {
    "selected_agent": "gmail",
    "reasoning": "The request involves sending an email, which falls under the email handling category.",
    "task_description": "Send an email to the specified address."
  },
  "recommended_agent": "gmail",
  "reasoning": "The request involves sending an email, which falls under the email handling category."
}
```

### Health Check
```http
GET /api/supervisor/health
```

### Agent Capabilities
```http
GET /api/supervisor/capabilities
```

### Agent Information
```http
GET /api/supervisor/agents
```

### Supervisor Statistics
```http
GET /api/supervisor/stats
```

## 🚀 Usage Examples

### 1. Calendar Operations

**Schedule a Meeting:**
```bash
curl -X POST "http://localhost:8000/api/supervisor/chat" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Schedule a meeting with amankumar.ak0012@gmail.com tomorrow at 4 PM"}'
```

**Check Calendar:**
```bash
curl -X POST "http://localhost:8000/api/supervisor/chat" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Check my calendar for tomorrow"}'
```

### 2. Email Operations

**Send Email:**
```bash
curl -X POST "http://localhost:8000/api/supervisor/chat" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Send an email to amankumar.ak0012@gmail.com with subject Test and body Hello"}'
```

**Search Emails:**
```bash
curl -X POST "http://localhost:8000/api/supervisor/chat" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Search for emails from amankumar.ak0098@gmail.com"}'
```

### 3. Complex Workflows

**Schedule and Send Invitation:**
```bash
curl -X POST "http://localhost:8000/api/supervisor/chat" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Schedule a meeting with amankumar.ak0098@gmail.com tomorrow at 5 PM and send an email invitation"}'
```

**Calendar Summary and Email:**
```bash
curl -X POST "http://localhost:8000/api/supervisor/chat" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Check my calendar for tomorrow and send a summary to amankumar.ak0098@gmail.com"}'
```

## 🔧 Testing

Run the supervisor agent tests:

```bash
python test_supervisor_agent.py
```

This will test:
- ✅ Supervisor agent creation
- ✅ Task analysis functionality
- ✅ Supervisor routing
- ✅ API endpoint functionality
- ✅ Agent capabilities

## 📊 Agent Capabilities

### Supervisor Agent
- Task analysis and classification
- Intelligent agent selection
- Workflow orchestration
- Result aggregation

### Calendar Agent
- Schedule events
- Delete events
- Reschedule events
- Check availability
- List events
- Suggest free slots

### Gmail Agent
- Send emails
- Read emails
- Search emails
- Reply to emails
- Forward emails
- Delete emails
- Manage labels

### Unified Agent
- All calendar capabilities
- All email capabilities
- Complex workflows
- Context awareness

## 🎯 Benefits

### 1. **Intelligent Routing**
- Automatically selects the most efficient agent
- Avoids using heavy unified agent for simple tasks
- Optimizes performance and cost

### 2. **Single Entry Point**
- One API endpoint for all operations
- Consistent interface across all agents
- Simplified client integration

### 3. **Fallback Strategy**
- Graceful error handling
- Automatic fallback to unified agent
- Robust error recovery

### 4. **Scalability**
- Easy to add new specialized agents
- Modular architecture
- Extensible design

## 🔄 Flow Diagram

```
User Request
    ↓
Supervisor Agent
    ↓
Task Analysis
    ↓
Agent Selection Decision
    ↓
┌─ Calendar Agent ──┐
├─ Gmail Agent ────┤
├─ Unified Agent ───┤
└─ Multi-Agent ────┘
    ↓
Execution & Tool Usage
    ↓
Service Layer (Calendar/Gmail APIs)
    ↓
Result Collection
    ↓
Response Aggregation
    ↓
Final Response to User
```

## 🛠️ Implementation Details

### Files Created
- `app/agents/supervisor_agent.py` - Main supervisor agent implementation
- `app/api/endpoints/supervisor.py` - API endpoints
- `test_supervisor_agent.py` - Test suite
- `SUPERVISOR_AGENT_README.md` - This documentation

### Key Features
- **JSON-based task analysis** with fallback keyword matching
- **Intelligent agent selection** based on task complexity
- **Comprehensive error handling** with fallback strategies
- **Detailed response format** with reasoning and analysis
- **Health monitoring** and capability reporting

## 🚀 Getting Started

1. **Start the server:**
   ```bash
   python -m uvicorn app.main:app --reload
   ```

2. **Test the supervisor:**
   ```bash
   python test_supervisor_agent.py
   ```

3. **Use the API:**
   ```bash
   curl -X POST "http://localhost:8000/api/supervisor/chat" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Schedule a meeting tomorrow at 2 PM"}'
   ```

## 📈 Performance

The supervisor agent provides:
- **Faster response times** for simple tasks (direct routing)
- **Cost optimization** (uses specialized agents when possible)
- **Better user experience** (intelligent task handling)
- **Scalable architecture** (easy to add new agents)

## 🔍 Monitoring

Monitor supervisor performance through:
- `/api/supervisor/health` - Health status
- `/api/supervisor/stats` - Performance metrics
- `/api/supervisor/capabilities` - Available capabilities

## 🎉 Success!

Your supervisor agent is now ready to intelligently route tasks to the most appropriate agent, providing a seamless experience for calendar and email management! 