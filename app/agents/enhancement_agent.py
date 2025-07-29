# app/agents/enhancement_agent.py

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from typing import Dict, Optional
from app.config import OPENAI_API_KEY

class EnhancementAgent:
    """Enhancement agent that improves user input with more context and details"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3,  # Slightly higher for creativity
            openai_api_key=OPENAI_API_KEY,
        )
        
        # Create the enhancement prompt
        self.enhancement_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an Enhancement Agent that improves user input by adding context, details, and clarity. Your goal is to make the user's request more specific and actionable.

## ENHANCEMENT RULES:

### 1. **Add Missing Context**
- If user mentions "meeting" → specify what type of meeting
- If user mentions "email" → suggest subject and content
- If user mentions "tomorrow" → specify the actual date
- If user mentions "team" → suggest specific email addresses

### 2. **Improve Specificity**
- Vague: "Schedule a meeting" → Enhanced: "Schedule a team meeting for project discussion"
- Vague: "Send email" → Enhanced: "Send a follow-up email with meeting summary"
- Vague: "Check calendar" → Enhanced: "Check my calendar for available slots this week"

### 3. **Add Relevant Details**
- Include suggested times if not specified
- Add location suggestions for meetings
- Include email templates for common scenarios
- Suggest follow-up actions

### 4. **Maintain Original Intent**
- Don't change the core request
- Keep the same action but make it more specific
- Preserve any specific details the user provided

## ENHANCEMENT EXAMPLES:

**Input**: "Schedule a meeting"
**Enhanced**: "Schedule a team meeting for tomorrow at 2 PM to discuss the project timeline"

**Input**: "Send email to john"
**Enhanced**: "Send a follow-up email to john@company.com with the meeting summary and action items"

**Input**: "Check my calendar"
**Enhanced**: "Check my calendar for tomorrow and list all scheduled meetings"

**Input**: "Schedule meeting and send invitation"
**Enhanced**: "Schedule a team meeting for tomorrow at 3 PM and send email invitations to all team members with meeting details"

## RESPONSE FORMAT:
You must respond with ONLY a valid JSON object in this exact format:
{
    "enhanced_input": "The enhanced user input with more context and details",
    "original_input": "The original user input",
    "enhancements_made": [
        "List of specific enhancements made",
        "e.g., Added specific time",
        "e.g., Suggested meeting type",
        "e.g., Included email template"
    ],
    "confidence_score": 0.95,
    "reasoning": "Brief explanation of why these enhancements were made"
}

IMPORTANT: Respond with ONLY the JSON object, no additional text or explanations.

Current date and time: {current_datetime}
"""),
            ("human", "{input}"),
        ])

    def enhance_input(self, user_input: str) -> Dict:
        """Enhance user input with more context and details"""
        try:
            # Get current datetime for context
            from app.tools.time_tool import get_current_datetime_tool
            current_datetime = get_current_datetime_tool.invoke({})
            
            # Create enhancement prompt
            response = self.llm.invoke(
                self.enhancement_prompt.format(
                    input=user_input,
                    current_datetime=current_datetime
                )
            )
            
            print(f"🔍 LLM Response: {response.content[:200]}...")
            
            # Try to extract JSON from response
            try:
                import re
                import json
                
                # Look for JSON in the response with better regex
                json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
                json_matches = re.findall(json_pattern, response.content, re.DOTALL)
                
                for json_str in json_matches:
                    try:
                        result = json.loads(json_str)
                        
                        # Validate required fields
                        required_fields = ["enhanced_input", "original_input", "enhancements_made", "confidence_score", "reasoning"]
                        if all(field in result for field in required_fields):
                            print(f"✅ JSON parsed successfully: {result['enhanced_input']}")
                            return result
                    except json.JSONDecodeError:
                        continue
                
                # If no valid JSON found, try fallback
                return self._fallback_enhancement(user_input, response.content)
                    
            except Exception as e:
                print(f"❌ JSON parsing error: {str(e)}")
                return self._fallback_enhancement(user_input, response.content)
                
        except Exception as e:
            return self._fallback_enhancement(user_input, f"Enhancement failed: {str(e)}")

    def _fallback_enhancement(self, user_input: str, llm_response: str) -> Dict:
        """Fallback enhancement when LLM response parsing fails"""
        # Simple keyword-based enhancements
        enhanced_input = user_input
        enhancements_made = []
        
        # Add time context if missing
        if "tomorrow" in user_input.lower() and "at" not in user_input.lower():
            enhanced_input += " at 2 PM"
            enhancements_made.append("Added default time (2 PM)")
        
        # Add meeting type if vague
        if "meeting" in user_input.lower() and "team" not in user_input.lower() and "project" not in user_input.lower():
            enhanced_input = enhanced_input.replace("meeting", "team meeting")
            enhancements_made.append("Specified meeting type (team meeting)")
        
        # Add email context if vague
        if "email" in user_input.lower() and "send" in user_input.lower() and "to" not in user_input.lower():
            enhanced_input += " to team members"
            enhancements_made.append("Added recipient context")
        
        # Add calendar context if vague
        if "calendar" in user_input.lower() and "check" in user_input.lower() and "for" not in user_input.lower():
            enhanced_input += " for tomorrow"
            enhancements_made.append("Added time context (tomorrow)")
        
        return {
            "enhanced_input": enhanced_input,
            "original_input": user_input,
            "enhancements_made": enhancements_made,
            "confidence_score": 0.7,
            "reasoning": f"Fallback enhancement applied. LLM response: {llm_response[:100]}..."
        }

    def get_enhancement_capabilities(self) -> Dict:
        """Get information about enhancement capabilities"""
        return {
            "enhancement_agent": {
                "description": "Input enhancement and context addition",
                "capabilities": [
                    "Add missing context and details",
                    "Improve request specificity",
                    "Suggest relevant information",
                    "Maintain original intent",
                    "Add time and date context",
                    "Suggest meeting types and locations",
                    "Provide email templates",
                    "Add recipient suggestions"
                ],
                "enhancement_types": {
                    "calendar_enhancements": [
                        "Add specific times",
                        "Suggest meeting types",
                        "Add location details",
                        "Include participant suggestions"
                    ],
                    "email_enhancements": [
                        "Add subject lines",
                        "Provide email templates",
                        "Suggest recipients",
                        "Include content suggestions"
                    ],
                    "context_enhancements": [
                        "Add date/time context",
                        "Specify vague terms",
                        "Include follow-up actions",
                        "Add priority indicators"
                    ]
                }
            }
        }

# Create global enhancement instance
enhancement_agent = EnhancementAgent()

def enhance_user_input(user_input: str) -> Dict:
    """Enhance user input with more context and details"""
    return enhancement_agent.enhance_input(user_input)

# Example usage
if __name__ == "__main__":
    # Test cases
    test_cases = [
        "Schedule a meeting",
        "Send email to john",
        "Check my calendar",
        "Schedule meeting and send invitation",
        "Send follow up email",
        "Book appointment"
    ]
    
    for test_case in test_cases:
        print(f"\n🤖 Original: {test_case}")
        result = enhance_user_input(test_case)
        print(f"✨ Enhanced: {result['enhanced_input']}")
        print(f"📝 Enhancements: {result['enhancements_made']}")
        print(f"🎯 Confidence: {result['confidence_score']}")
        print(f"💭 Reasoning: {result['reasoning']}")
        print("-" * 50) 