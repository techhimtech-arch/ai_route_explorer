#!/usr/bin/env python3
"""
Simple test script to verify .env configuration is loaded correctly
"""

import os
from dotenv import load_dotenv

print("=" * 60)
print("🔍 Environment Configuration Test")
print("=" * 60)

# Load environment variables
load_dotenv()

# Check all required keys
required_keys = {
    "OPENROUTE_API_KEY": "OpenRouteService API Key",
    "OLLAMA_URL": "Ollama URL",
    "OLLAMA_MODEL": "Ollama Model Name",
}

optional_keys = {
    "TAVILY_API_KEY": "Tavily API Key (Optional)",
    "GOOGLE_PLACES_API_KEY": "Google Places API Key (Optional)",
}

all_good = True

print("\n✅ REQUIRED CONFIGURATION:")
print("-" * 60)
for key, description in required_keys.items():
    value = os.getenv(key)
    if value:
        # Show only first 20 chars for security
        display_value = value[:20] + "..." if len(value) > 20 else value
        print(f"  ✓ {key:25} = {display_value}")
    else:
        print(f"  ✗ {key:25} = NOT SET ❌")
        all_good = False

print("\n⚠️  OPTIONAL CONFIGURATION:")
print("-" * 60)
for key, description in optional_keys.items():
    value = os.getenv(key)
    if value:
        display_value = value[:20] + "..." if len(value) > 20 else value
        print(f"  ✓ {key:25} = {display_value}")
    else:
        print(f"  - {key:25} = Not configured")

print("\n" + "=" * 60)
if all_good:
    print("✅ All required keys are configured!")
    print("🚀 Ready to run: streamlit run app.py")
else:
    print("❌ Some required keys are missing!")
    print("📝 Please update .env file with your API keys")
print("=" * 60)
