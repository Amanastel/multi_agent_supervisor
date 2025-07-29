# app/agents/supervisor_agent.py

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import Dict, List, Optional, Tuple
import json
from app.agents.calendar_agent import get_calendar_agent
from app.agents.gmail_agent import run_gmail_agent
from app.agents.unified_agent import run_unified_agent
from app.agents.enhancement_agent import enhance_user_input
from app.config import OPENAI_API_KEY

class SupervisorAgent:
    """Supervisor agent that intelligently routes tasks to appropriate agents"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.1,
            openai_api_key=OPENAI_API_KEY,
        )
        
        # Initialize sub-agents
        self.calendar_agent = get_calendar_agent()
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        
        # Create the supervisor prompt
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a Supervisor Agent that intelligently routes tasks to the most appropriate agent. You have access to three specialized agents:

## AVAILABLE AGENTS:

### 1. Calendar Agent
- **Best for**: Pure calendar operations
- **Capabilities**: Schedule, delete, reschedule, check availability, list events
- **Use when**: User only mentions calendar/meeting/scheduling tasks

### 2. Gmail Agent  
- **Best for**: Pure email operations
- **Capabilities**: Send, read, search, reply, forward, delete emails
- **Use when**: User only mentions email/mail/sending tasks

### 3. Unified Agent
- **Best for**: Complex workflows involving both calendar and email
- **Capabilities**: Everything from both Calendar and Gmail agents
- **Use when**: User mentions both calendar AND email in same request

## ROUTING DECISION LOGIC:

1. **Calendar-only tasks**: Use Calendar Agent
   - "Schedule a meeting tomorrow"
   - "Check my availability"
   - "List my events"

2. **Email-only tasks**: Use Gmail Agent
   - "Send an email to john@example.com"
   - "Search for emails from alice"
   - "Reply to the latest email"

3. **Complex/Combined tasks**: Use Unified Agent
   - "Schedule a meeting and send invitation"
   - "Check calendar and send summary to team"
   - "Reschedule meeting and notify attendees"

## RESPONSE FORMAT:
Always respond with a JSON object containing:
{
    "selected_agent": "calendar|gmail|unified",
    "reasoning": "Brief explanation of why this agent was chosen",
    "task_description": "What task will be performed"
}

Current date and time: {current_datetime}
"""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Create the supervisor agent
        self.agent = create_openai_tools_agent(
            llm=self.llm,
            tools=[],  # Supervisor doesn't need tools, it routes to other agents
            prompt=self.prompt
        )
        
        self.supervisor_executor = AgentExecutor(
            agent=self.agent,
            tools=[],
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=5
        )

    def analyze_task(self, user_input: str) -> Dict:
        """Analyze the task and determine which agent to use"""
        try:
            # Create a simple prompt for task analysis
            analysis_prompt = f"""
            Analyze this user request and determine which agent should handle it:
            
            User Request: "{user_input}"
            
            You must respond with ONLY a valid JSON object in this exact format:
            {{
                "selected_agent": "calendar",
                "reasoning": "Brief explanation",
                "task_description": "What task will be performed"
            }}
            
            Choose the agent based on these rules:
            - Use "calendar" for scheduling, meetings, events, availability
            - Use "gmail" for emails, sending, searching emails
            - Use "unified" for tasks involving both calendar AND email
            """
            
            response = self.llm.invoke(analysis_prompt)
            
            # Try to extract JSON from response
            try:
                # Look for JSON in the response
                import re
                json_match = re.search(r'\{.*\}', response.content, re.DOTALL)
                if json_match:
                    parsed = json.loads(json_match.group())
                    # Validate the selected_agent
                    if parsed.get("selected_agent") in ["calendar", "gmail", "unified"]:
                        return parsed
                    else:
                        return self._parse_response_fallback(response.content, user_input)
                else:
                    # Fallback parsing
                    return self._parse_response_fallback(response.content, user_input)
            except json.JSONDecodeError:
                return self._parse_response_fallback(response.content, user_input)
                
        except Exception as e:
            # Fallback to unified agent if analysis fails
            return {
                "selected_agent": "unified",
                "reasoning": f"Analysis failed: {str(e)}. Using unified agent as fallback.",
                "task_description": user_input
            }

    def _parse_response_fallback(self, response_text: str, user_input: str) -> Dict:
        """Fallback parsing when JSON extraction fails"""
        response_lower = response_text.lower()
        
        # Simple keyword-based routing
        calendar_keywords = ["schedule", "meeting", "calendar", "event", "availability", "reschedule"]
        email_keywords = ["email", "send", "mail", "gmail", "reply", "forward"]
        
        calendar_score = sum(1 for keyword in calendar_keywords if keyword in user_input.lower())
        email_score = sum(1 for keyword in email_keywords if keyword in user_input.lower())
        
        if calendar_score > 0 and email_score > 0:
            return {
                "selected_agent": "unified",
                "reasoning": "Both calendar and email keywords detected",
                "task_description": user_input
            }
        elif calendar_score > 0:
            return {
                "selected_agent": "calendar",
                "reasoning": "Calendar-related keywords detected",
                "task_description": user_input
            }
        elif email_score > 0:
            return {
                "selected_agent": "gmail",
                "reasoning": "Email-related keywords detected",
                "task_description": user_input
            }
        else:
            return {
                "selected_agent": "unified",
                "reasoning": "No clear keywords detected, using unified agent",
                "task_description": user_input
            }

    def should_enhance_input(self, user_input: str) -> Dict:
        """Decide whether the user input needs enhancement"""
        try:
            # Create a simple prompt to determine if enhancement is needed
            enhancement_prompt = f"""Analyze this user input and determine if it needs enhancement:

User Input: "{user_input}"

Consider these factors:
1. **Clarity**: Is the request clear and specific?
2. **Context**: Does it have enough context (time, recipients, details)?
3. **Completeness**: Are all necessary details provided?
4. **Ambiguity**: Could this be interpreted in multiple ways?

Respond with ONLY a JSON object:
{{
    "needs_enhancement": true/false,
    "reasoning": "Brief explanation of why enhancement is or isn't needed",
    "confidence": 0.95
}}

Examples:
- "Schedule meeting" → needs_enhancement: true (missing time, attendees, purpose)
- "Send email to john@example.com about project update" → needs_enhancement: false (clear and specific)
- "Check calendar" → needs_enhancement: false (simple and clear)
- "Meeting tomorrow" → needs_enhancement: true (missing details)
"""

            response = self.llm.invoke(enhancement_prompt)
            
            # Parse JSON response
            import re
            json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
            json_matches = re.findall(json_pattern, response.content, re.DOTALL)
            
            for json_str in json_matches:
                try:
                    parsed = json.loads(json_str)
                    if "needs_enhancement" in parsed:
                        return parsed
                except json.JSONDecodeError:
                    continue
            
            # Fallback: simple keyword-based decision
            vague_keywords = ["meeting", "email", "schedule", "send", "check", "tomorrow", "later"]
            has_vague_keywords = any(keyword in user_input.lower() for keyword in vague_keywords)
            
            return {
                "needs_enhancement": has_vague_keywords,
                "reasoning": f"Fallback decision based on vague keywords: {vague_keywords}",
                "confidence": 0.7
            }
            
        except Exception as e:
            # Conservative fallback - enhance if unsure
            return {
                "needs_enhancement": True,
                "reasoning": f"Error in enhancement analysis: {str(e)}. Defaulting to enhance.",
                "confidence": 0.5
            }

    def route_to_agent(self, user_input: str) -> Dict:
        """Route the task to the appropriate agent and execute"""
        
        # Step 1: Decide if enhancement is needed
        enhancement_decision = self.should_enhance_input(user_input)
        needs_enhancement = enhancement_decision.get("needs_enhancement", True)
        
        print(f"🤔 Enhancement Decision:")
        print(f"   Needs Enhancement: {needs_enhancement}")
        print(f"   Reasoning: {enhancement_decision['reasoning']}")
        print(f"   Confidence: {enhancement_decision['confidence']}")
        
        # Step 2: Enhance if needed
        if needs_enhancement:
            enhancement_result = enhance_user_input(user_input)
            enhanced_input = enhancement_result["enhanced_input"]
            
            print(f"✨ Enhancement Applied:")
            print(f"   Original: {enhancement_result['original_input']}")
            print(f"   Enhanced: {enhancement_result['enhanced_input']}")
            print(f"   Enhancements: {enhancement_result['enhancements_made']}")
        else:
            # No enhancement needed
            enhancement_result = {
                "enhanced_input": user_input,
                "original_input": user_input,
                "enhancements_made": ["No enhancement needed - input was clear"],
                "confidence_score": 1.0,
                "reasoning": "Input was clear and specific"
            }
            enhanced_input = user_input
            
            print(f"✨ No Enhancement Needed:")
            print(f"   Input was clear and specific")
        
        # Step 3: Analyze the task (enhanced or original)
        analysis = self.analyze_task(enhanced_input)
        selected_agent = analysis["selected_agent"]
        
        print(f"🔍 Supervisor Analysis:")
        print(f"   Selected Agent: {selected_agent}")
        print(f"   Reasoning: {analysis['reasoning']}")
        print(f"   Task: {analysis['task_description']}")
        
        # Step 4: Route to appropriate agent
        try:
            if selected_agent == "calendar":
                result = self.calendar_agent.invoke({"input": enhanced_input})
                response = result["output"] if isinstance(result, dict) else str(result)
                
            elif selected_agent == "gmail":
                response = run_gmail_agent(enhanced_input)
                
            elif selected_agent == "unified":
                response = run_unified_agent(enhanced_input)
                
            else:
                # Fallback to unified agent
                response = run_unified_agent(enhanced_input)
                selected_agent = "unified"
            
            return {
                "success": True,
                "response": response,
                "selected_agent": selected_agent,
                "analysis": analysis,
                "enhancement_decision": enhancement_decision,
                "enhancement": enhancement_result
            }
            
        except Exception as e:
            # Fallback to unified agent if routing fails
            try:
                response = run_unified_agent(enhanced_input)
                return {
                    "success": True,
                    "response": response,
                    "selected_agent": "unified",
                    "analysis": {
                        "selected_agent": "unified",
                        "reasoning": f"Routing failed: {str(e)}. Using unified agent as fallback.",
                        "task_description": enhanced_input
                    },
                    "enhancement_decision": enhancement_decision,
                    "enhancement": enhancement_result
                }
            except Exception as fallback_error:
                return {
                    "success": False,
                    "response": f"❌ Error: {str(fallback_error)}",
                    "selected_agent": "unified",
                    "analysis": {
                        "selected_agent": "unified",
                        "reasoning": f"All agents failed: {str(fallback_error)}",
                        "task_description": enhanced_input
                    },
                    "enhancement_decision": enhancement_decision,
                    "enhancement": enhancement_result
                }

    def get_agent_capabilities(self) -> Dict:
        """Get information about all available agents"""
        return {
            "supervisor": {
                "description": "Intelligent task router and orchestrator",
                "capabilities": [
                    "Task analysis and classification",
                    "Intelligent agent selection",
                    "Workflow orchestration",
                    "Result aggregation"
                ]
            },
            "enhancement": {
                "description": "Input enhancement and context addition",
                "capabilities": [
                    "Add missing context and details",
                    "Improve request specificity",
                    "Suggest relevant information",
                    "Maintain original intent"
                ]
            },
            "calendar": {
                "description": "Specialized calendar operations",
                "capabilities": [
                    "Schedule events",
                    "Delete events", 
                    "Reschedule events",
                    "Check availability",
                    "List events",
                    "Suggest free slots"
                ]
            },
            "gmail": {
                "description": "Specialized email operations",
                "capabilities": [
                    "Send emails",
                    "Read emails",
                    "Search emails",
                    "Reply to emails",
                    "Forward emails",
                    "Delete emails",
                    "Manage labels"
                ]
            },
            "unified": {
                "description": "Combined calendar and email operations",
                "capabilities": [
                    "All calendar capabilities",
                    "All email capabilities", 
                    "Complex workflows",
                    "Context awareness"
                ]
            }
        }

# Create global supervisor instance
supervisor_agent = SupervisorAgent()

def run_supervisor_agent(user_input: str) -> Dict:
    """Run the supervisor agent with user input"""
    return supervisor_agent.route_to_agent(user_input)

# Example usage
if __name__ == "__main__":
    # Test cases
    test_cases = [
        "Schedule a meeting tomorrow at 2 PM",
        "Send an email to john@example.com",
        "Schedule a meeting and send an email invitation",
        "Check my calendar for tomorrow",
        "What emails do I have from alice@company.com?"
    ]
    
    for test_case in test_cases:
        print(f"\n🤖 Testing: {test_case}")
        result = run_supervisor_agent(test_case)
        print(f"📊 Result: {result}")
        print("-" * 50) 