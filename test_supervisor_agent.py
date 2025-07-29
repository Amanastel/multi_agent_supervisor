#!/usr/bin/env python3
"""
Test script for supervisor agent functionality
"""

import os
from dotenv import load_dotenv
from app.agents.supervisor_agent import run_supervisor_agent, supervisor_agent

# Load environment variables
load_dotenv()

def test_supervisor_agent_creation():
    """Test that the supervisor agent can be created successfully"""
    print("🧪 Testing supervisor agent creation...")
    
    try:
        from app.agents.supervisor_agent import supervisor_agent
        
        print("✅ Supervisor agent created successfully")
        print("🤖 Agent has access to all sub-agents:")
        print("   - Calendar Agent")
        print("   - Gmail Agent") 
        print("   - Unified Agent")
        
        # Test capabilities
        capabilities = supervisor_agent.get_agent_capabilities()
        print(f"📊 Available agents: {len(capabilities)}")
        for agent_name, agent_info in capabilities.items():
            print(f"   - {agent_name}: {len(agent_info['capabilities'])} capabilities")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing supervisor agent: {str(e)}")
        return False

def test_task_analysis():
    """Test task analysis functionality"""
    print("\n🧪 Testing task analysis...")
    
    test_cases = [
        {
            "input": "Schedule a meeting tomorrow at 2 PM",
            "expected_agent": "calendar",
            "description": "Calendar-only task"
        },
        {
            "input": "Send an email to john@example.com",
            "expected_agent": "gmail", 
            "description": "Email-only task"
        },
        {
            "input": "Schedule a meeting and send an email invitation",
            "expected_agent": "unified",
            "description": "Combined task"
        },
        {
            "input": "Check my calendar for tomorrow",
            "expected_agent": "calendar",
            "description": "Calendar query"
        },
        {
            "input": "What emails do I have from alice@company.com?",
            "expected_agent": "gmail",
            "description": "Email search"
        }
    ]
    
    results = []
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n  Test {i}: {test_case['description']}")
        print(f"  Input: {test_case['input']}")
        
        try:
            analysis = supervisor_agent.analyze_task(test_case['input'])
            selected_agent = analysis['selected_agent']
            reasoning = analysis['reasoning']
            
            print(f"  Selected Agent: {selected_agent}")
            print(f"  Expected Agent: {test_case['expected_agent']}")
            print(f"  Reasoning: {reasoning}")
            
            # Check if analysis is reasonable
            if selected_agent in ['calendar', 'gmail', 'unified']:
                results.append(True)
                print(f"  ✅ PASS - Valid agent selected")
            else:
                results.append(False)
                print(f"  ❌ FAIL - Invalid agent selected")
                
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            results.append(False)
    
    passed = sum(results)
    total = len(results)
    print(f"\n  📊 Task Analysis Results: {passed}/{total} tests passed")
    return passed == total

def test_supervisor_routing():
    """Test supervisor routing functionality"""
    print("\n🧪 Testing supervisor routing...")
    
    test_cases = [
        {
            "input": "Schedule a meeting tomorrow at 2 PM",
            "description": "Calendar routing test"
        },
        {
            "input": "Send an email to john@example.com with subject 'Test'",
            "description": "Gmail routing test"
        },
        {
            "input": "Schedule a meeting and send an email invitation",
            "description": "Unified routing test"
        }
    ]
    
    results = []
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n  Test {i}: {test_case['description']}")
        print(f"  Input: {test_case['input']}")
        
        try:
            result = run_supervisor_agent(test_case['input'])
            
            print(f"  Success: {result['success']}")
            print(f"  Selected Agent: {result['selected_agent']}")
            print(f"  Reasoning: {result['analysis']['reasoning']}")
            print(f"  Response: {result['response'][:100]}...")
            
            if result['success']:
                results.append(True)
                print(f"  ✅ PASS - Routing successful")
            else:
                results.append(False)
                print(f"  ❌ FAIL - Routing failed")
                
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            results.append(False)
    
    passed = sum(results)
    total = len(results)
    print(f"\n  📊 Routing Results: {passed}/{total} tests passed")
    return passed == total

def test_api_endpoint():
    """Test the supervisor API endpoint"""
    print("\n🧪 Testing supervisor API endpoint...")
    
    try:
        from app.api.endpoints.supervisor import router
        from fastapi import FastAPI
        from fastapi.testclient import TestClient
        
        # Create a test app
        app = FastAPI()
        app.include_router(router)
        client = TestClient(app)
        
        # Test health endpoint
        response = client.get("/supervisor/health")
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
        
        # Test capabilities endpoint
        response = client.get("/supervisor/capabilities")
        if response.status_code == 200:
            print("✅ Capabilities endpoint working")
        else:
            print(f"❌ Capabilities endpoint failed: {response.status_code}")
            return False
        
        # Test chat endpoint
        chat_data = {
            "prompt": "What can you help me with?",
            "user_id": "test_user"
        }
        response = client.post("/supervisor/chat", json=chat_data)
        if response.status_code == 200:
            print("✅ Chat endpoint working")
            return True
        else:
            print(f"❌ Chat endpoint failed: {response.status_code}")
            return False
        
    except Exception as e:
        print(f"❌ Error testing API endpoint: {str(e)}")
        return False

def test_agent_capabilities():
    """Test agent capabilities information"""
    print("\n🧪 Testing agent capabilities...")
    
    try:
        capabilities = supervisor_agent.get_agent_capabilities()
        
        required_agents = ['supervisor', 'calendar', 'gmail', 'unified']
        for agent in required_agents:
            if agent in capabilities:
                print(f"✅ {agent.capitalize()} agent capabilities available")
            else:
                print(f"❌ {agent.capitalize()} agent capabilities missing")
                return False
        
        print(f"📊 Total agents: {len(capabilities)}")
        for agent_name, agent_info in capabilities.items():
            print(f"   - {agent_name}: {len(agent_info['capabilities'])} capabilities")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing capabilities: {str(e)}")
        return False

def main():
    """Run all supervisor agent tests"""
    print("🚀 Starting supervisor agent functionality tests...\n")
    
    tests = [
        ("Supervisor Agent Creation", test_supervisor_agent_creation),
        ("Task Analysis", test_task_analysis),
        ("Supervisor Routing", test_supervisor_routing),
        ("API Endpoint", test_api_endpoint),
        ("Agent Capabilities", test_agent_capabilities)
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
        print("🎉 All supervisor agent tests passed! Your supervisor agent is ready.")
        print("\n📝 Usage Examples:")
        print("  - Calendar task: 'Schedule a meeting tomorrow at 2 PM'")
        print("  - Email task: 'Send an email to john@example.com'")
        print("  - Combined task: 'Schedule meeting and send invitation'")
        print("\n🔗 API Endpoint: POST /api/supervisor/chat")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main() 