# Gmail Integration

This document explains how to set up and use the Gmail integration in your multi-agent supervisor system.

## 🚀 Features

The Gmail integration provides the following capabilities:

### 📧 Email Operations
- **Send emails** with subject, body, CC, and BCC
- **Read emails** by ID with full content extraction
- **Search emails** using Gmail search syntax
- **Get recent emails** with filtering options
- **Reply to emails** with automatic threading
- **Forward emails** to other recipients
- **Delete emails** by ID
- **Mark emails as read/unread**

### 🏷️ Label Management
- **Get all Gmail labels** for organization
- **Filter emails by labels**

### 🤖 AI Assistant
- **Gmail Agent** with natural language processing
- **Conversational interface** for email management
- **Context-aware responses** with memory

## 📋 Prerequisites

1. **Google Cloud Project** with Gmail API enabled
2. **OAuth 2.0 credentials** for Gmail API access
3. **Access token** with Gmail API scopes

### Required Gmail API Scopes
```
https://www.googleapis.com/auth/gmail.send
https://www.googleapis.com/auth/gmail.readonly
https://www.googleapis.com/auth/gmail.modify
https://www.googleapis.com/auth/gmail.labels
```

## 🔧 Setup Instructions

### 1. Environment Variables

Add the following to your `.env` file:

```bash
# Gmail API
GOOGLE_GMAIL_TOKEN=your_gmail_access_token_here
```

### 2. Get Gmail Access Token

#### Option A: Using Google Cloud Console
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Gmail API
4. Create OAuth 2.0 credentials
5. Download the credentials JSON file
6. Use Google's OAuth 2.0 playground or a script to get access token

#### Option B: Using Google OAuth 2.0 Playground
1. Visit [Google OAuth 2.0 Playground](https://developers.google.com/oauthplayground/)
2. Click the settings icon (⚙️) in the top right
3. Check "Use your own OAuth credentials"
4. Enter your OAuth 2.0 client ID and client secret
5. Close settings
6. Select Gmail API v1 from the list
7. Select the required scopes:
   - `https://www.googleapis.com/auth/gmail.send`
   - `https://www.googleapis.com/auth/gmail.readonly`
   - `https://www.googleapis.com/auth/gmail.modify`
   - `https://www.googleapis.com/auth/gmail.labels`
8. Click "Authorize APIs"
9. Click "Exchange authorization code for tokens"
10. Copy the access token to your `.env` file

### 3. Test the Setup

Run the test script to verify everything is working:

```bash
python test_gmail.py
```

## 📚 Usage Examples

### Using the Gmail Agent

```python
from app.agents.gmail_agent import run_gmail_agent

# Send an email
response = run_gmail_agent("Send an email to john@example.com with subject 'Meeting' and body 'Hi John, let's meet tomorrow.'")

# Get recent emails
response = run_gmail_agent("Get my recent emails")

# Search for emails
response = run_gmail_agent("Search for emails from alice@company.com")

# Reply to an email
response = run_gmail_agent("Reply to email ID 12345 with message 'Thanks for the update!'")
```

### Using Gmail Tools Directly

```python
from app.tools.gmail_tool import send_email_tool, get_emails_tool

# Send email
result = send_email_tool.invoke({
    "to": "recipient@example.com",
    "subject": "Test Email",
    "body": "This is a test email"
})

# Get emails
result = get_emails_tool.invoke({
    "max_results": 10,
    "query": "is:unread"
})
```

### Using the API Endpoints

```bash
# Send email
curl -X POST "http://localhost:8000/api/gmail/send" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "recipient@example.com",
    "subject": "Test Email",
    "body": "This is a test email"
  }'

# Get emails
curl -X POST "http://localhost:8000/api/gmail/get" \
  -H "Content-Type: application/json" \
  -d '{
    "max_results": 10
  }'

# Search emails
curl -X POST "http://localhost:8000/api/gmail/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "from:john@example.com",
    "max_results": 5
  }'
```

## 🛠️ API Endpoints

### POST `/api/gmail/send`
Send an email
```json
{
  "to": "recipient@example.com",
  "subject": "Email Subject",
  "body": "Email body content",
  "cc": "cc@example.com",
  "bcc": "bcc@example.com"
}
```

### POST `/api/gmail/get`
Get emails with optional filtering
```json
{
  "query": "is:unread",
  "max_results": 10,
  "label": "INBOX"
}
```

### POST `/api/gmail/read`
Read a specific email by ID
```json
{
  "email_id": "email_id_here"
}
```

### POST `/api/gmail/search`
Search emails using Gmail search syntax
```json
{
  "query": "from:john@example.com subject:meeting",
  "max_results": 10
}
```

### DELETE `/api/gmail/delete`
Delete an email by ID
```json
{
  "email_id": "email_id_here"
}
```

### POST `/api/gmail/reply`
Reply to an email
```json
{
  "email_id": "email_id_here",
  "reply_body": "Your reply message"
}
```

### POST `/api/gmail/forward`
Forward an email
```json
{
  "email_id": "email_id_here",
  "forward_to": "newrecipient@example.com",
  "additional_message": "Optional additional message"
}
```

### GET `/api/gmail/labels`
Get all Gmail labels (no body required)

### POST `/api/gmail/mark-read`
Mark an email as read
```json
{
  "email_id": "email_id_here"
}
```

### POST `/api/gmail/mark-unread`
Mark an email as unread
```json
{
  "email_id": "email_id_here"
}
```

## 🔍 Gmail Search Syntax

The Gmail integration supports Gmail's powerful search syntax:

- `from:john@example.com` - Emails from specific sender
- `to:alice@company.com` - Emails sent to specific recipient
- `subject:meeting` - Emails with "meeting" in subject
- `is:unread` - Unread emails
- `is:read` - Read emails
- `has:attachment` - Emails with attachments
- `label:important` - Emails with specific label
- `after:2024/01/01` - Emails after specific date
- `before:2024/12/31` - Emails before specific date

## 🛡️ Security Considerations

1. **Token Security**: Keep your Gmail access token secure and never commit it to version control
2. **Token Expiration**: Gmail access tokens expire. You'll need to refresh them periodically
3. **Scope Limitation**: Only request the scopes you actually need
4. **Rate Limiting**: Be mindful of Gmail API rate limits

## 🐛 Troubleshooting

### Common Issues

1. **"Invalid Credentials" Error**
   - Check that your `GOOGLE_GMAIL_TOKEN` is correct
   - Verify the token hasn't expired
   - Ensure the token has the required scopes

2. **"Permission Denied" Error**
   - Verify your OAuth 2.0 credentials are correct
   - Check that Gmail API is enabled in your Google Cloud project
   - Ensure the user has granted the necessary permissions

3. **"Quota Exceeded" Error**
   - Gmail API has rate limits
   - Implement exponential backoff for retries
   - Consider caching results when appropriate

### Debug Mode

Enable verbose logging by setting the agent's `verbose=True`:

```python
gmail_agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,  # Enable debug output
    handle_parsing_errors=True,
    max_iterations=10
)
```

## 📈 Performance Tips

1. **Batch Operations**: When possible, batch multiple operations
2. **Caching**: Cache frequently accessed data like labels
3. **Pagination**: Use `max_results` parameter to limit response size
4. **Error Handling**: Implement proper error handling and retries

## 🔄 Token Refresh

Gmail access tokens expire. To handle token refresh:

1. Store both access token and refresh token
2. Implement token refresh logic
3. Update the stored token when it expires
4. Consider using Google's client libraries for automatic refresh

## 📝 License

This Gmail integration is part of the multi-agent supervisor system and follows the same license terms. 