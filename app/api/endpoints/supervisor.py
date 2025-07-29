# app/api/endpoints/supervisor.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
from app.agents.supervisor_agent import run_supervisor_agent, supervisor_agent

router = APIRouter(prefix="/supervisor", tags=["supervisor"])

class SupervisorRequest(BaseModel):
    prompt: str
    user_id: Optional[str] = None
    preferred_agent: Optional[str] = None  # "auto", "calendar", "gmail", "unified"

class SupervisorResponse(BaseModel):
    response: str
    success: bool
    selected_agent: str
    reasoning: str
    task_description: str
    enhancement_decision: Optional[Dict] = None
    enhancement: Optional[Dict] = None
    error: Optional[str] = None

@router.post("/chat", response_model=SupervisorResponse)
async def supervisor_chat_endpoint(request: SupervisorRequest):
    """
    Main supervisor endpoint that intelligently routes tasks to appropriate agents.
    
    This endpoint provides intelligent task routing to:
    - Calendar Agent: For calendar-only operations
    - Gmail Agent: For email-only operations  
    - Unified Agent: For complex workflows involving both
    
    Examples:
    - "Schedule a meeting tomorrow" → Calendar Agent
    - "Send an email to john@example.com" → Gmail Agent
    - "Schedule meeting and send invitation" → Unified Agent
    """
    try:
        # Run the supervisor agent
        result = run_supervisor_agent(request.prompt)
        
        return SupervisorResponse(
            response=result["response"],
            success=result["success"],
            selected_agent=result["analysis"]["selected_agent"],
            reasoning=result["analysis"]["reasoning"],
            task_description=result["analysis"]["task_description"],
            enhancement_decision=result.get("enhancement_decision"),
            enhancement=result.get("enhancement"),
            error=result.get("error")
        )
        
    except Exception as e:
        return SupervisorResponse(
            response="I encountered an error while processing your request.",
            success=False,
            selected_agent="unified",
            reasoning=f"Error occurred: {str(e)}",
            task_description=request.prompt,
            enhancement_decision=None,
            enhancement=None,
            error=str(e)
        )

@router.get("/health")
async def health_check():
    """Health check endpoint for the supervisor agent"""
    return {
        "status": "healthy",
        "service": "supervisor-agent",
        "capabilities": [
            "intelligent-task-routing",
            "agent-orchestration",
            "workflow-management"
        ],
        "available_agents": [
            "calendar",
            "gmail", 
            "unified"
        ]
    }

@router.get("/capabilities")
async def get_capabilities():
    """Get detailed information about all available agents and their capabilities"""
    return supervisor_agent.get_agent_capabilities()

@router.get("/agents")
async def get_agents():
    """Get information about available agents"""
    return {
        "supervisor": {
            "description": "Intelligent task router and orchestrator",
            "endpoint": "/api/supervisor/chat"
        },
        "calendar": {
            "description": "Specialized calendar operations",
            "endpoint": "/api/calendar/schedule"
        },
        "gmail": {
            "description": "Specialized email operations", 
            "endpoints": [
                "/api/gmail/send",
                "/api/gmail/get",
                "/api/gmail/search",
                "/api/gmail/reply",
                "/api/gmail/forward",
                "/api/gmail/delete",
                "/api/gmail/labels"
            ]
        },
        "unified": {
            "description": "Combined calendar and email operations",
            "endpoint": "/api/unified/chat"
        }
    }

@router.post("/analyze")
async def analyze_task(request: SupervisorRequest):
    """Analyze a task without executing it"""
    try:
        analysis = supervisor_agent.analyze_task(request.prompt)
        return {
            "success": True,
            "analysis": analysis,
            "recommended_agent": analysis["selected_agent"],
            "reasoning": analysis["reasoning"]
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "analysis": {
                "selected_agent": "unified",
                "reasoning": f"Analysis failed: {str(e)}",
                "task_description": request.prompt
            }
        }

@router.get("/stats")
async def get_supervisor_stats():
    """Get supervisor agent statistics and performance metrics"""
    return {
        "supervisor": {
            "status": "active",
            "version": "1.0.0",
            "capabilities": [
                "Task analysis and classification",
                "Intelligent agent selection", 
                "Workflow orchestration",
                "Result aggregation"
            ]
        },
        "routing_logic": {
            "calendar_keywords": [
                "schedule", "meeting", "calendar", "event", 
                "availability", "reschedule", "appointment"
            ],
            "email_keywords": [
                "email", "send", "mail", "gmail", "reply", 
                "forward", "message", "inbox"
            ],
            "complex_keywords": [
                "and", "then", "also", "additionally", "follow up"
            ]
        },
        "fallback_strategy": {
            "primary": "unified_agent",
            "reason": "Handles all task types"
        }
    } 