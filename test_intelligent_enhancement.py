#!/usr/bin/env python3
"""
Test script to demonstrate intelligent enhancement decision making
by the Supervisor Agent.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.agents.supervisor_agent import SupervisorAgent

def test_enhancement_decisions():
    """Test various inputs to see if enhancement is needed"""
    
    print("🧪 Testing Intelligent Enhancement Decision Making")
    print("=" * 60)
    
    # Initialize supervisor agent
    supervisor = SupervisorAgent()
    
    # Test cases with different levels of clarity
    test_cases = [
        # Clear inputs (should NOT need enhancement)
        {
            "input": "Send email to john@example.com about project update",
            "expected": False,
            "description": "Clear and specific email request"
        },
        {
            "input": "Check my calendar for tomorrow",
            "expected": False,
            "description": "Clear calendar check request"
        },
        {
            "input": "Schedule meeting with team on Friday at 2pm",
            "expected": False,
            "description": "Specific meeting request with time"
        },
        
        # Vague inputs (should need enhancement)
        {
            "input": "Schedule meeting",
            "expected": True,
            "description": "Vague meeting request"
        },
        {
            "input": "Send email",
            "expected": True,
            "description": "Vague email request"
        },
        {
            "input": "Meeting tomorrow",
            "expected": True,
            "description": "Incomplete meeting details"
        },
        {
            "input": "Check calendar",
            "expected": True,
            "description": "Vague calendar request"
        },
        {
            "input": "Send to john",
            "expected": True,
            "description": "Incomplete email request"
        }
    ]
    
    print("\n📋 Testing Enhancement Decision Logic:")
    print("-" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['description']}")
        print(f"   Input: '{test_case['input']}'")
        
        # Test enhancement decision
        decision = supervisor.should_enhance_input(test_case['input'])
        
        print(f"   Decision: {decision['needs_enhancement']}")
        print(f"   Reasoning: {decision['reasoning']}")
        print(f"   Confidence: {decision['confidence']}")
        
        # Check if decision matches expectation
        if decision['needs_enhancement'] == test_case['expected']:
            print(f"   ✅ PASS - Decision matches expectation")
        else:
            print(f"   ❌ FAIL - Expected {test_case['expected']}, got {decision['needs_enhancement']}")

def test_complete_flow():
    """Test the complete flow with enhancement decision"""
    
    print("\n\n🔄 Testing Complete Flow with Enhancement Decision")
    print("=" * 60)
    
    # Initialize supervisor agent
    supervisor = SupervisorAgent()
    
    # Test cases for complete flow
    flow_test_cases = [
        {
            "input": "Schedule meeting",
            "description": "Vague request that should be enhanced"
        },
        {
            "input": "Send email to john@example.com about project update",
            "description": "Clear request that should NOT be enhanced"
        },
        {
            "input": "Meeting tomorrow",
            "description": "Incomplete request that should be enhanced"
        }
    ]
    
    for i, test_case in enumerate(flow_test_cases, 1):
        print(f"\n{i}. {test_case['description']}")
        print(f"   Input: '{test_case['input']}'")
        print("-" * 40)
        
        # Run complete flow
        result = supervisor.route_to_agent(test_case['input'])
        
        print(f"   Success: {result['success']}")
        print(f"   Selected Agent: {result['selected_agent']}")
        print(f"   Enhancement Decision: {result['enhancement_decision']['needs_enhancement']}")
        print(f"   Enhancement Applied: {len(result['enhancement']['enhancements_made'])} enhancements")
        print(f"   Response: {result['response'][:100]}...")

def test_api_endpoint():
    """Test the API endpoint with enhancement decision"""
    
    print("\n\n🌐 Testing API Endpoint with Enhancement Decision")
    print("=" * 60)
    
    import requests
    import json
    
    # Test the API endpoint
    test_inputs = [
        "Schedule meeting",
        "Send email to john@example.com about project update",
        "Meeting tomorrow"
    ]
    
    for i, user_input in enumerate(test_inputs, 1):
        print(f"\n{i}. Testing: '{user_input}'")
        
        try:
            response = requests.post(
                "http://localhost:8000/api/supervisor/chat",
                json={"prompt": user_input},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Success")
                print(f"   Selected Agent: {result['selected_agent']}")
                print(f"   Enhancement Decision: {result.get('enhancement_decision', {}).get('needs_enhancement', 'N/A')}")
                print(f"   Response: {result['response'][:100]}...")
            else:
                print(f"   ❌ Error: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("   ❌ Connection Error: Make sure the server is running")
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting Intelligent Enhancement Decision Tests")
    print("=" * 60)
    
    # Test 1: Enhancement decision logic
    test_enhancement_decisions()
    
    # Test 2: Complete flow
    test_complete_flow()
    
    # Test 3: API endpoint (if server is running)
    print("\n" + "=" * 60)
    print("💡 To test the API endpoint, make sure the server is running:")
    print("   python3 -m uvicorn app.main:app --reload")
    print("=" * 60)
    
    # Uncomment to test API endpoint
    # test_api_endpoint()
    
    print("\n✅ All tests completed!") 