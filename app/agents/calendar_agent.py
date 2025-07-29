# app/agents/calendar_agent.py
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.tools.calendar_tool import calendar_tool, calendar_delete_tool, calendar_get_events_tool, reschedule_event_tool, check_availability_tool, list_day_events_tool, suggest_free_slots_tool
from app.tools.time_tool import extract_datetime, get_current_datetime_tool




def get_calendar_agent() -> AgentExecutor:
    llm = ChatOpenAI(temperature=0)
    tools = [
    calendar_tool,
    calendar_delete_tool,
    calendar_get_events_tool,
    reschedule_event_tool,
    check_availability_tool,
    list_day_events_tool,
    suggest_free_slots_tool,
    extract_datetime,
    get_current_datetime_tool
]


    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a calendar assistant. Use tools to help the user."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),  # REQUIRED for tool-using agents
    ])

    agent = create_openai_functions_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    return AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True
    )