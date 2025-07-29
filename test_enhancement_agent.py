#!/usr/bin/env python3
"""
Test script for enhancement agent functionality
"""

import os
from dotenv import load_dotenv
from app.agents.enhancement_agent import enhance_user_input, enhancement_agent

# Load environment variables
load_dotenv()

def test_enhancement_agent_creation():
    """Test that the enhancement agent can be created successfully"""
    print("🧪 Testing enhancement agent creation...")
    
    try:
        from app.agents.enhancement_agent import enhancement_agent
        
        print("✅ Enhancement agent created successfully")
        
        # Test capabilities
        capabilities = enhancement_agent.get_enhancement_capabilities()
        print(f"📊 Enhancement capabilities: {len(capabilities['enhancement_agent']['capabilities'])}")
        for capability in capabilities['enhancement_agent']['capabilities']:
            print(f"   - {capability}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing enhancement agent: {str(e)}")
        return False

def test_enhancement_functionality():
    """Test enhancement functionality with various inputs"""
    print("\n🧪 Testing enhancement functionality...")
    
    test_cases = [
        {
            "input": "Schedule a meeting",
            "expected_enhancements": ["time", "type", "context"]
        },
        {
            "input": "Send email to john",
            "expected_enhancements": ["subject", "content", "email"]
        },
        {
            "input": "Check my calendar",
            "expected_enhancements": ["time", "context"]
        },
        {
            "input": "Schedule meeting and send invitation",
            "expected_enhancements": ["time", "type", "recipients"]
        },
        {
            "input": "Send follow up email",
            "expected_enhancements": ["recipient", "subject", "content"]
        }
    ]
    
    results = []
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n  Test {i}: {test_case['input']}")
        
        try:
            result = enhance_user_input(test_case['input'])
            
            print(f"  Original: {result['original_input']}")
            print(f"  Enhanced: {result['enhanced_input']}")
            print(f"  Enhancements: {result['enhancements_made']}")
            print(f"  Confidence: {result['confidence_score']}")
            print(f"  Reasoning: {result['reasoning']}")
            
            # Check if enhancements were made
            if len(result['enhancements_made']) > 0:
                results.append(True)
                print(f"  ✅ PASS - Enhancements applied")
            else:
                results.append(False)
                print(f"  ❌ FAIL - No enhancements made")
                
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            results.append(False)
    
    passed = sum(results)
    total = len(results)
    print(f"\n  📊 Enhancement Results: {passed}/{total} tests passed")
    return passed == total

def test_enhancement_integration():
    """Test enhancement integration with supervisor agent"""
    print("\n🧪 Testing enhancement integration...")
    
    try:
        from app.agents.supervisor_agent import run_supervisor_agent
        
        test_cases = [
            "Schedule a meeting",
            "Send email to team",
            "Check calendar"
        ]
        
        results = []
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n  Test {i}: {test_case}")
            
            try:
                result = run_supervisor_agent(test_case)
                
                print(f"  Success: {result['success']}")
                print(f"  Selected Agent: {result['selected_agent']}")
                print(f"  Response: {result['response'][:100]}...")
                
                # Check if enhancement was included
                if 'enhancement' in result:
                    enhancement = result['enhancement']
                    print(f"  Enhancement Applied: ✅")
                    print(f"    Original: {enhancement['original_input']}")
                    print(f"    Enhanced: {enhancement['enhanced_input']}")
                    print(f"    Enhancements: {enhancement['enhancements_made']}")
                    results.append(True)
                else:
                    print(f"  Enhancement Applied: ❌")
                    results.append(False)
                    
            except Exception as e:
                print(f"  ❌ Error: {str(e)}")
                results.append(False)
        
        passed = sum(results)
        total = len(results)
        print(f"\n  📊 Integration Results: {passed}/{total} tests passed")
        return passed == total
        
    except Exception as e:
        print(f"❌ Error testing integration: {str(e)}")
        return False

def test_enhancement_api():
    """Test enhancement through API endpoint"""
    print("\n🧪 Testing enhancement API endpoint...")
    
    try:
        from app.api.endpoints.supervisor import router
        from fastapi import FastAPI
        from fastapi.testclient import TestClient
        
        # Create a test app
        app = FastAPI()
        app.include_router(router)
        client = TestClient(app)
        
        # Test supervisor endpoint with enhancement
        chat_data = {
            "prompt": "Schedule a meeting",
            "user_id": "test_user"
        }
        response = client.post("/supervisor/chat", json=chat_data)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API endpoint working")
            
            if 'enhancement' in data:
                enhancement = data['enhancement']
                print(f"  Enhancement Applied: ✅")
                print(f"    Original: {enhancement['original_input']}")
                print(f"    Enhanced: {enhancement['enhanced_input']}")
                return True
            else:
                print(f"  Enhancement Applied: ❌")
                return False
        else:
            print(f"❌ API endpoint failed: {response.status_code}")
            return False
        
    except Exception as e:
        print(f"❌ Error testing API: {str(e)}")
        return False

def test_enhancement_capabilities():
    """Test enhancement agent capabilities"""
    print("\n🧪 Testing enhancement capabilities...")
    
    try:
        capabilities = enhancement_agent.get_enhancement_capabilities()
        
        required_sections = ['enhancement_agent']
        for section in required_sections:
            if section in capabilities:
                print(f"✅ {section.capitalize()} capabilities available")
            else:
                print(f"❌ {section.capitalize()} capabilities missing")
                return False
        
        enhancement_agent_info = capabilities['enhancement_agent']
        print(f"📊 Enhancement types: {len(enhancement_agent_info['enhancement_types'])}")
        for enhancement_type, capabilities_list in enhancement_agent_info['enhancement_types'].items():
            print(f"   - {enhancement_type}: {len(capabilities_list)} capabilities")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing capabilities: {str(e)}")
        return False

def main():
    """Run all enhancement agent tests"""
    print("🚀 Starting enhancement agent functionality tests...\n")
    
    tests = [
        ("Enhancement Agent Creation", test_enhancement_agent_creation),
        ("Enhancement Functionality", test_enhancement_functionality),
        ("Enhancement Integration", test_enhancement_integration),
        ("Enhancement API", test_enhancement_api),
        ("Enhancement Capabilities", test_enhancement_capabilities)
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
        print("🎉 All enhancement agent tests passed! Your enhancement agent is ready.")
        print("\n📝 Enhancement Examples:")
        print("  - 'Schedule a meeting' → 'Schedule a team meeting for tomorrow at 2 PM'")
        print("  - 'Send email to john' → 'Send a follow-up email to john@company.com'")
        print("  - 'Check calendar' → 'Check my calendar for tomorrow'")
        print("\n🔗 API Endpoint: POST /api/supervisor/chat (now includes enhancement)")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main() 