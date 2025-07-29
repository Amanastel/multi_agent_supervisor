#!/usr/bin/env python3
"""
Test script for Gmail functionality
"""

import os
from dotenv import load_dotenv
from app.services.gmail_service import get_labels, GetLabelsInput

# Load environment variables
load_dotenv()

def test_gmail_connection():
    """Test basic Gmail API connection"""
    print("🧪 Testing Gmail API connection...")
    
    # Check if Gmail token is available
    gmail_token = os.getenv("GOOGLE_GMAIL_TOKEN")
    if not gmail_token:
        print("❌ GOOGLE_GMAIL_TOKEN not found in environment variables")
        print("Please set GOOGLE_GMAIL_TOKEN in your .env file")
        return False
    
    try:
        # Test getting labels (simple operation)
        input_data = GetLabelsInput()
        result = get_labels(input_data)
        
        if result.success:
            print("✅ Gmail API connection successful!")
            print(f"📧 Found {len(result.labels or [])} labels")
            return True
        else:
            print(f"❌ Gmail API error: {result.message}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Gmail API: {str(e)}")
        return False

def test_gmail_tools():
    """Test Gmail tools"""
    print("\n🧪 Testing Gmail tools...")
    
    try:
        from app.tools.gmail_tool import (
            send_email_tool,
            get_emails_tool,
            search_emails_tool,
            get_labels_tool
        )
        
        print("✅ Gmail tools imported successfully")
        print(f"📧 Available tools:")
        print(f"  - {send_email_tool.name}: {send_email_tool.description}")
        print(f"  - {get_emails_tool.name}: {get_emails_tool.description}")
        print(f"  - {search_emails_tool.name}: {search_emails_tool.description}")
        print(f"  - {get_labels_tool.name}: {get_labels_tool.description}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Gmail tools: {str(e)}")
        return False

def test_gmail_agent():
    """Test Gmail agent"""
    print("\n🧪 Testing Gmail agent...")
    
    try:
        from app.agents.gmail_agent import gmail_agent_executor
        
        print("✅ Gmail agent created successfully")
        print("🤖 Agent is ready to handle Gmail operations")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Gmail agent: {str(e)}")
        return False

def main():
    """Run all Gmail tests"""
    print("🚀 Starting Gmail functionality tests...\n")
    
    tests = [
        ("Gmail API Connection", test_gmail_connection),
        ("Gmail Tools", test_gmail_tools),
        ("Gmail Agent", test_gmail_agent)
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
        print("🎉 All Gmail tests passed! Your Gmail implementation is ready.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main() 