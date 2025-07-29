# app/agents/unified_agent.py

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.tools.calendar_tool import (
    calendar_tool,
    calendar_delete_tool,
    calendar_get_events_tool,
    reschedule_event_tool,
    check_availability_tool,
    list_day_events_tool,
    suggest_free_slots_tool
)
from app.tools.gmail_tool import (
    send_email_tool,
    get_emails_tool,
    read_email_tool,
    search_emails_tool,
    delete_email_tool,
    reply_to_email_tool,
    forward_email_tool,
    get_labels_tool,
    mark_as_read_tool,
    mark_as_unread_tool
)
from app.tools.time_tool import extract_datetime, get_current_datetime_tool
from app.config import OPENAI_API_KEY

# Initialize the language model
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.1,
    openai_api_key=OPENAI_API_KEY,
)

# Create the prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful AI assistant that can manage both calendar events and emails. You have access to various tools for both Gmail and Google Calendar operations.

## CALENDAR CAPABILITIES:
- Schedule calendar events with title, date, time, and location
- Delete calendar events by title, date, and time
- Get events for a date range
- Reschedule existing events
- Check availability for specific times
- List events for a specific day
- Suggest free time slots for meetings

## GMAIL CAPABILITIES:
- Send emails with subject, body, CC, and BCC
- Read and search emails using Gmail search syntax
- Reply to emails with automatic threading
- Forward emails to other recipients
- Delete emails by ID
- Manage email labels and read/unread status
- Get email information and details

## WORKFLOW GUIDELINES:
1. **Understand the user's intent** - Are they asking about calendar or email operations?
2. **Ask for clarification** when needed - Don't assume details
3. **Provide clear explanations** of what you're doing
4. **Handle errors gracefully** and suggest alternatives
5. **Remember context** - Use previous conversation to understand follow-up requests
6. **Be proactive** - Suggest related actions when appropriate

## EXAMPLES:
- "Schedule a meeting with John tomorrow at 2 PM" → Use calendar tools
- "Send an email to john@example.com about the meeting" → Use Gmail tools
- "Check my calendar for tomorrow and send a summary to the team" → Use both calendar and Gmail tools
- "What emails do I have from John?" → Use Gmail search tools
- "Reschedule my 3 PM meeting to 4 PM" → Use calendar tools
"""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Initialize memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Combine all tools
all_tools = [
    # Calendar tools
    calendar_tool,
    calendar_delete_tool,
    calendar_get_events_tool,
    reschedule_event_tool,
    check_availability_tool,
    list_day_events_tool,
    suggest_free_slots_tool,
    
    # Gmail tools
    send_email_tool,
    get_emails_tool,
    read_email_tool,
    search_emails_tool,
    delete_email_tool,
    reply_to_email_tool,
    forward_email_tool,
    get_labels_tool,
    mark_as_read_tool,
    mark_as_unread_tool,
    
    # Utility tools
    extract_datetime,
    get_current_datetime_tool
]

# Create the agent
agent = create_openai_tools_agent(
    llm=llm,
    tools=all_tools,
    prompt=prompt
)

# Create the agent executor
unified_agent_executor = AgentExecutor(
    agent=agent,
    tools=all_tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=15
)

def run_unified_agent(user_input: str) -> str:
    """Run the unified agent with user input"""
    try:
        result = unified_agent_executor.invoke({
            "input": user_input
        })
        return result["output"]
    except Exception as e:
        return f"❌ Error running unified agent: {str(e)}"

# Example usage
if __name__ == "__main__":
    # Example interactions
    examples = [
        "Schedule a meeting with John tomorrow at 2 PM in Conference Room A",
        "Send an email to john@example.com with subject 'Meeting Tomorrow' and body 'Hi John, I've scheduled our meeting for tomorrow at 2 PM.'",
        "Check my calendar for tomorrow and send a summary to the team",
        "What emails do I have from alice@company.com?",
        "Reschedule my 3 PM meeting to 4 PM",
        "Reply to the latest email from john@example.com with 'Thanks for the update!'"
    ]
    
    for example in examples:
        print(f"\n🤖 User: {example}")
        response = run_unified_agent(example)
        print(f"📧 Assistant: {response}")
        print("-" * 50) 