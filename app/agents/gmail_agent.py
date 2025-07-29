# app/agents/gmail_agent.py

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
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

# Initialize the language model
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.1,
    openai_api_key="sk-proj-...",  # Replace with your OpenAI API key
)

# Create the prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful Gmail assistant that can help users manage their emails. You have access to various Gmail tools and can:

1. Send emails to recipients
2. Read and search emails
3. Reply to and forward emails
4. Delete emails
5. Manage email labels and read/unread status
6. Get email information and details

When working with emails:
- Always be helpful and professional
- Ask for clarification if needed
- Provide clear explanations of what you're doing
- Handle errors gracefully and suggest alternatives
- Remember that email IDs are needed for specific operations like reading, replying, or deleting emails

Current date and time: {current_datetime}
"""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Initialize memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Create the agent
agent = create_openai_tools_agent(
    llm=llm,
    tools=[
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
        extract_datetime,
        get_current_datetime_tool
    ],
    prompt=prompt
)

# Create the agent executor
gmail_agent_executor = AgentExecutor(
    agent=agent,
    tools=[
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
        extract_datetime,
        get_current_datetime_tool
    ],
    memory=memory,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=10
)

def run_gmail_agent(user_input: str) -> str:
    """Run the Gmail agent with user input"""
    try:
        result = gmail_agent_executor.invoke({
            "input": user_input,
            "current_datetime": get_current_datetime_tool.invoke({})
        })
        return result["output"]
    except Exception as e:
        return f"❌ Error running Gmail agent: {str(e)}"

# Example usage
if __name__ == "__main__":
    # Example interactions
    examples = [
        "Send an email to john@example.com with subject 'Meeting Tomorrow' and body 'Hi John, let's meet tomorrow at 2 PM.'",
        "Get my recent emails",
        "Search for emails from alice@company.com",
        "Get all my Gmail labels",
        "Check what time it is"
    ]
    
    for example in examples:
        print(f"\n🤖 User: {example}")
        response = run_gmail_agent(example)
        print(f"📧 Assistant: {response}")
        print("-" * 50) 