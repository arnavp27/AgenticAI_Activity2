#!/usr/bin/env python3
"""
Quick test script to verify Gemini API key is working
Run this before running the main manufacturing system
"""

import os
import sys

def test_gemini_connection():
    """Test if Gemini API key is configured and working"""
    
    print("=" * 60)
    print("GEMINI API CONNECTION TEST")
    print("=" * 60)
    print()
    
    # Check if API key is set
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key or api_key == "your-gemini-api-key-here":
        print("❌ GEMINI_API_KEY not found or not configured!")
        print()
        print("Please set your API key using one of these methods:")
        print()
        print("Method 1 - Environment Variable:")
        print("  export GEMINI_API_KEY='your-actual-key'")
        print()
        print("Method 2 - Edit manufacturing_system.py:")
        print("  Change the GEMINI_API_KEY line to your actual key")
        print()
        print("Get your free API key at:")
        print("  https://makersuite.google.com/app/apikey")
        print()
        sys.exit(1)
    
    print(f"✓ API Key found: {api_key[:10]}...{api_key[-4:]}")
    print()
    
    # Try to import required packages
    print("Checking dependencies...")
    
    try:
        import google.generativeai as genai
        print("✓ google-generativeai installed")
    except ImportError:
        print("❌ google-generativeai not installed")
        print("   Run: pip install google-generativeai")
        sys.exit(1)
    
    try:
        from crewai import LLM
        print("✓ crewai installed")
    except ImportError:
        print("❌ crewai not installed")
        print("   Run: pip install crewai crewai-tools")
        sys.exit(1)
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        print("✓ langchain-google-genai installed")
    except ImportError:
        print("❌ langchain-google-genai not installed")
        print("   Run: pip install langchain-google-genai")
        sys.exit(1)
    
    print()
    print("Testing API connection...")
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Try a simple generation with gemini-flash-lite-latest
        model = genai.GenerativeModel('gemini-flash-lite-latest')
        response = model.generate_content("Say 'Connection successful!' in one sentence.")
        
        print("✓ API connection successful!")
        print(f"✓ Response: {response.text.strip()}")
        print()
        print("=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print()
        print("You're ready to run the manufacturing system:")
        print("  python manufacturing_system.py")
        print()
        
    except Exception as e:
        print(f"❌ API connection failed: {str(e)}")
        print()
        print("Possible issues:")
        print("  - Invalid API key")
        print("  - API key doesn't have proper permissions")
        print("  - Network connectivity issues")
        print("  - Gemini API quota exceeded")
        print()
        print("Get a new API key at:")
        print("  https://makersuite.google.com/app/apikey")
        print()
        sys.exit(1)

if __name__ == "__main__":
    test_gemini_connection()