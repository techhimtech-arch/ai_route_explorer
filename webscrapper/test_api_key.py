#!/usr/bin/env python3
"""
Test OpenRouteService API key
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTE_API_KEY")

print("=" * 60)
print("🔍 Testing OpenRouteService API")
print("=" * 60)
print(f"\n📝 API Key: {API_KEY[:20]}...")

try:
    # Simple geocoding test
    url = "https://api.openrouteservice.org/geocode/search"
    params = {
        "api_key": API_KEY,
        "text": "shimla"
    }
    
    print(f"\n🌐 Requesting: {url}")
    print(f"📦 Params: {params}")
    
    response = requests.get(url, params=params, timeout=10)
    
    print(f"\n✓ Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ API Key is VALID!")
        data = response.json()
        print(f"\n📍 Results for 'shimla':")
        if data.get('features'):
            for feature in data['features'][:2]:
                props = feature.get('properties', {})
                print(f"  - {props.get('name')} ({props.get('county')})")
    
    elif response.status_code == 403:
        print("❌ API Key is INVALID or EXPIRED!")
        print("\n💡 Solutions:")
        print("  1. नया API key generate करो: https://openrouteservice.org/register")
        print("  2. .env file में update करो:")
        print("     OPENROUTE_API_KEY=your_new_key_here")
        print("  3. फिर से app run करो")
    
    else:
        print(f"⚠️ Error: {response.status_code}")
        print(f"Message: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 60)
