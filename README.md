# Multi-Agent Supervisor System

This project is a multi-agent supervisor system built with Python, leveraging LangChain and LangGraph for orchestrating intelligent agents. The system is designed to automate and enhance workflows involving calendar and email operations, with modular agents for each domain and a supervisor agent for intelligent routing.

## Features

- **Supervisor Agent**: Routes user requests to the most appropriate agent (Calendar, Gmail, Unified) based on task analysis.
- **Enhancement Agent**: Improves user input by adding context, details, and clarity, making requests more specific and actionable.
- **Gmail Agent**: Manages email operations such as sending, reading, searching, replying, forwarding, and deleting emails using Gmail tools.
- **Calendar Agent**: Handles calendar operations including scheduling, deleting, rescheduling, checking availability, and listing events.
- **Unified Agent**: Manages complex workflows that involve both calendar and email operations.
- **Tool Integration**: Modular tools for calendar, Gmail, datetime, and time operations.
- **Schema & Services**: Structured schemas and service layers for calendar and Gmail data management.

## Technologies Used

- Python 3.11+
- LangChain
- LangGraph
- OpenAI API
- Google Calendar & Gmail APIs

## Setup

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your `.env` file with the required API keys and tokens:
   - `OPENAI_API_KEY`
   - `GOOGLE_CALENDAR_TOKEN`
   - `GOOGLE_GMAIL_TOKEN`
4. Run the main application:
   ```bash
   python app/main.py
   ```

## Directory Structure

- `app/agents/` — Agent implementations (calendar, gmail, enhancement, supervisor, unified)
- `app/tools/` — Modular tools for agent operations
- `app/services/` — Service layers for calendar and Gmail
- `app/schema/` — Data schemas for calendar and Gmail
- `app/api/endpoints/` — API endpoints for agent interaction
- `app/config.py` — Configuration and environment variables
- `app/main.py` — Entry point for the application

## Usage

- Interact with the supervisor agent to automate calendar and email workflows.
- The enhancement agent will automatically improve vague or incomplete requests.
- Agents communicate and route tasks based on user input and context.

## Example Requests

- "Schedule a meeting tomorrow at 2 PM and send invitations to the team."
- "Send a follow-up email to john@company.com with the meeting summary."
- "Check my calendar for available slots this week."

## License

MIT License
