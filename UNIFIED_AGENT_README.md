# Unified Agent - Calendar & Gmail Assistant

This document explains how to use the unified agent that combines both calendar and Gmail functionality into a single intelligent assistant.

## 🚀 Overview

The unified agent provides a single conversational interface for managing both your Google Calendar and Gmail. Instead of using separate agents for calendar and email operations, you can now interact with one intelligent assistant that understands context and can perform complex workflows involving both services.

## 🎯 Key Features

### 📅 Calendar Operations
- Schedule events with title, date, time, and location
- Delete events by title, date, and time
- Get events for a date range
- Reschedule existing events
- Check availability for specific times
- List events for a specific day
- Suggest free time slots for meetings

### 📧 Gmail Operations
- Send emails with subject, body, CC, and BCC
- Read and search emails using Gmail search syntax
- Reply to emails with automatic threading
- Forward emails to other recipients
- Delete emails by ID
- Manage email labels and read/unread status
- Get email information and details

### 🔄 Combined Workflows
- Check calendar and send email summaries
- Create calendar events from email content
- Schedule meetings and send invitations
- Send follow-up emails after meetings
- Coordinate between calendar and email seamlessly

## 🛠️ API Endpoints

### POST `/api/unified/chat`
Main chat endpoint for all operations.

**Request:**
```json
{
  "prompt": "Schedule a meeting with John tomorrow at 2 PM",
  "user_id": "optional_user_id"
}
```

**Response:**
```json
{
  "response": "I've scheduled a meeting with John for tomorrow at 2:00 PM. The event has been added to your calendar.",
  "success": true,
  "error": null
}
```

### GET `/api/unified/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "unified-agent",
  "capabilities": [
    "calendar-management",
    "email-management",
    "combined-workflows"
  ]
}
```

### GET `/api/unified/capabilities`
Get detailed information about available capabilities.

## 📚 Usage Examples

### Basic Calendar Operations

```bash
# Schedule a meeting
curl -X POST "http://localhost:8000/api/unified/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Schedule a meeting with John tomorrow at 2 PM in Conference Room A"
  }'

# Check availability
curl -X POST "http://localhost:8000/api/unified/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Check if I'm available tomorrow at 3 PM"
  }'

# Reschedule an event
curl -X POST "http://localhost:8000/api/unified/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Reschedule my 3 PM meeting to 4 PM"
  }'
```

### Basic Gmail Operations

```bash
# Send an email
curl -X POST "http://localhost:8000/api/unified/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Send an email to john@example.com with subject 'Meeting Tomorrow' and body 'Hi John, I've scheduled our meeting for tomorrow at 2 PM.'"
  }'

# Search emails
curl -X POST "http://localhost:8000/api/unified/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What emails do I have from alice@company.com?"
  }'

# Reply to an email
curl -X POST "http://localhost:8000/api/unified/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Reply to the latest email from john@example.com with 'Thanks for the update!'"
  }'
```

### Combined Workflows

```bash
# Check calendar and send summary
curl -X POST "http://localhost:8000/api/unified/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Check my calendar for tomorrow and send a summary to the team"
  }'

# Schedule meeting and send invitation
curl -X POST "http://localhost:8000/api/unified/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Schedule a team meeting for Friday at 10 AM and send invitations to john@example.com and alice@company.com"
  }'

# Follow up after meeting
curl -X POST "http://localhost:8000/api/unified/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Send a follow-up email to all attendees of my 2 PM meeting with the action items"
  }'
```

## 🔍 Advanced Usage

### Gmail Search Syntax

The unified agent supports Gmail's powerful search syntax:

- `from:john@example.com` - Emails from specific sender
- `to:alice@company.com` - Emails sent to specific recipient
- `subject:meeting` - Emails with "meeting" in subject
- `is:unread` - Unread emails
- `is:read` - Read emails
- `has:attachment` - Emails with attachments
- `label:important` - Emails with specific label
- `after:2024/01/01` - Emails after specific date
- `before:2024/12/31` - Emails before specific date

### Date and Time Formats

- **Dates**: Use `YYYY-MM-DD` format or natural language like "tomorrow", "next Friday"
- **Times**: Use `HH:MM` format or natural language like "2 PM", "3:30 PM"

### Context Awareness

The unified agent maintains conversation context, so you can use follow-up requests:

```
User: "Schedule a meeting with John tomorrow at 2 PM"
Assistant: "I've scheduled a meeting with John for tomorrow at 2:00 PM."

User: "Send him an email about the meeting"
Assistant: "I'll send an email to John about the meeting we just scheduled."
```

## 🐛 Troubleshooting

### Common Issues

1. **"Invalid Credentials" Error**
   - Check that your `GOOGLE_CALENDAR_TOKEN` and `GOOGLE_GMAIL_TOKEN` are correct
   - Verify the tokens haven't expired
   - Ensure the tokens have the required scopes

2. **"Permission Denied" Error**
   - Verify your OAuth 2.0 credentials are correct
   - Check that Gmail API and Calendar API are enabled in your Google Cloud project
   - Ensure the user has granted the necessary permissions

3. **"Tool not found" Error**
   - The agent should automatically select the appropriate tools
   - If you get this error, try rephrasing your request more clearly

### Debug Mode

Enable verbose logging by setting the agent's `verbose=True`:

```python
unified_agent_executor = AgentExecutor(
    agent=agent,
    tools=all_tools,
    memory=memory,
    verbose=True,  # Enable debug output
    handle_parsing_errors=True,
    max_iterations=15
)
```

## 📈 Performance Tips

1. **Be Specific**: Provide clear, specific instructions for better results
2. **Use Natural Language**: The agent understands natural language, so be conversational
3. **Provide Context**: Include relevant details like names, times, and locations
4. **Follow-up Requests**: Use the conversation context for related requests

## 🔄 Migration from Separate Agents

If you were previously using separate calendar and Gmail agents, the unified agent provides several advantages:

### Before (Separate Agents)
```python
# Calendar operations
from app.agents.calendar_agent import run_calendar_agent
result = run_calendar_agent("Schedule a meeting with John tomorrow at 2 PM")

# Gmail operations  
from app.agents.gmail_agent import run_gmail_agent
result = run_gmail_agent("Send an email to john@example.com about the meeting")
```

### After (Unified Agent)
```python
# All operations in one agent
from app.agents.unified_agent import run_unified_agent

# Calendar operation
result = run_unified_agent("Schedule a meeting with John tomorrow at 2 PM")

# Gmail operation
result = run_unified_agent("Send an email to john@example.com about the meeting")

# Combined workflow
result = run_unified_agent("Schedule a meeting with John tomorrow at 2 PM and send him an email invitation")
```

## 🛡️ Security Considerations

1. **Token Security**: Keep your access tokens secure and never commit them to version control
2. **Token Expiration**: Access tokens expire. You'll need to refresh them periodically
3. **Scope Limitation**: Only request the scopes you actually need
4. **Rate Limiting**: Be mindful of API rate limits

## 📝 License

This unified agent is part of the multi-agent supervisor system and follows the same license terms. 