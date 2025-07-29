#!/usr/bin/env python3
"""
Test script for unified agent functionality
"""

import os
from dotenv import load_dotenv
from app.agents.unified_agent import run_unified_agent

# Load environment variables
load_dotenv()

def test_unified_agent_creation():
    """Test that the unified agent can be created successfully"""
    print("🧪 Testing unified agent creation...")
    
    try:
        from app.agents.unified_agent import unified_agent_executor
        
        print("✅ Unified agent created successfully")
        print("🤖 Agent has access to both calendar and Gmail tools")
        
        # Check available tools
        tool_names = [tool.name for tool in unified_agent_executor.tools]
        calendar_tools = [name for name in tool_names if 'calendar' in name.lower() or 'event' in name.lower()]
        gmail_tools = [name for name in tool_names if 'email' in name.lower() or 'gmail' in name.lower()]
        
        print(f"📅 Calendar tools: {len(calendar_tools)}")
        print(f"📧 Gmail tools: {len(gmail_tools)}")
        print(f"🔧 Total tools: {len(tool_names)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing unified agent: {str(e)}")
        return False

def test_unified_agent_functionality():
    """Test basic unified agent functionality"""
    print("\n🧪 Testing unified agent functionality...")
    
    # Test cases that should work even without API tokens
    test_cases = [
        {
            "input": "What can you help me with?",
            "description": "Basic capability inquiry"
        },
        {
            "input": "Tell me about your calendar and email capabilities",
            "description": "Capability explanation"
        },
        {
            "input": "How do I schedule a meeting?",
            "description": "Calendar guidance"
        },
        {
            "input": "How do I send an email?",
            "description": "Email guidance"
        }
    ]
    
    results = []
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n  Test {i}: {test_case['description']}")
        print(f"  Input: {test_case['input']}")
        
        try:
            response = run_unified_agent(test_case['input'])
            print(f"  Response: {response[:100]}...")
            results.append(True)
        except Exception as e:
            print(f"  Error: {str(e)}")
            results.append(False)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\n  📊 Results: {passed}/{total} tests passed")
    return passed == total

def test_api_endpoint():
    """Test the unified API endpoint"""
    print("\n🧪 Testing unified API endpoint...")
    
    try:
        from app.api.endpoints.unified import router
        from fastapi import FastAPI
        from fastapi.testclient import TestClient
        
        # Create a test app
        app = FastAPI()
        app.include_router(router)
        client = TestClient(app)
        
        # Test health endpoint
        response = client.get("/unified/health")
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
        
        # Test capabilities endpoint
        response = client.get("/unified/capabilities")
        if response.status_code == 200:
            print("✅ Capabilities endpoint working")
        else:
            print(f"❌ Capabilities endpoint failed: {response.status_code}")
            return False
        
        # Test chat endpoint (should work even without tokens)
        chat_data = {
            "prompt": "What can you help me with?",
            "user_id": "test_user"
        }
        response = client.post("/unified/chat", json=chat_data)
        if response.status_code == 200:
            print("✅ Chat endpoint working")
            return True
        else:
            print(f"❌ Chat endpoint failed: {response.status_code}")
            return False
        
    except Exception as e:
        print(f"❌ Error testing API endpoint: {str(e)}")
        return False

def main():
    """Run all unified agent tests"""
    print("🚀 Starting unified agent functionality tests...\n")
    
    tests = [
        ("Unified Agent Creation", test_unified_agent_creation),
        ("Unified Agent Functionality", test_unified_agent_functionality),
        ("Unified API Endpoint", test_api_endpoint)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"Running {test_name} test...")
        result = test_func()
        results.append((test_name, result))
        print()
    
    # Summary
    print("📊 Test Results:")
    print("=" * 50)
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All unified agent tests passed! Your unified agent is ready.")
        print("\n📝 Usage Examples:")
        print("  - Schedule a meeting: 'Schedule a meeting with John tomorrow at 2 PM'")
        print("  - Send an email: 'Send an email to john@example.com about the meeting'")
        print("  - Combined workflow: 'Check my calendar for tomorrow and send a summary to the team'")
        print("  - Search emails: 'What emails do I have from alice@company.com?'")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main() 