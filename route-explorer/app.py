"""
AI Route Explorer - Main Streamlit Application
Finds businesses and places along your route
"""

import streamlit as st
import os
from dotenv import load_dotenv
from services import RouteService, AIService, SearchService
from utils import format_distance, format_duration

# Load environment variables from .env file
load_dotenv()

# ==================== Configuration ====================
# API Key from environment
API_KEY = os.getenv("OPENROUTE_API_KEY")
if not API_KEY:
    st.error("❌ OPENROUTE_API_KEY not found in .env file")
    st.stop()

# Initialize services
route_service = RouteService(API_KEY)
ai_service = AIService()
search_service = SearchService()

# ==================== Page Configuration ====================
st.set_page_config(
    page_title="AI Route Explorer",
    page_icon="🗺️",
    layout="wide"
)

# ==================== UI Layout ====================
st.title("🗺️ AI Route Explorer")
st.markdown("Find businesses and places along your route powered by AI")

# ==================== Input Section ====================
st.markdown("### 📍 Enter Your Route Details")
col1, col2, col3 = st.columns(3)

with col1:
    source = st.text_input("From", placeholder="e.g., Shimla")

with col2:
    destination = st.text_input("To", placeholder="e.g., Paonta Sahib")

with col3:
    search_query = st.text_input("What to find", placeholder="e.g., plant nurseries")

# ==================== Search Button & Processing ====================
if st.button("🔍 Search Route & Places", type="primary"):
    if not source or not destination or not search_query:
        st.error("❌ Please fill in all fields")
    else:
        with st.spinner("Processing your route..."):
            
            # Step 1: Geocode source location
            st.info("Step 1: Finding source location...")
            source_data = route_service.geocode_location(source)
            
            if not source_data:
                st.error(f"❌ Could not find location: {source}")
                st.stop()
            
            # Step 2: Geocode destination location
            st.info("Step 2: Finding destination location...")
            dest_data = route_service.geocode_location(destination)
            
            if not dest_data:
                st.error(f"❌ Could not find location: {destination}")
                st.stop()
            
            # Step 3: Get route between locations
            st.info("Step 3: Calculating route...")
            source_coords = (source_data["longitude"], source_data["latitude"])
            dest_coords = (dest_data["longitude"], dest_data["latitude"])
            
            route_data = route_service.get_route(source_coords, dest_coords)
            
            if not route_data:
                st.error("❌ Could not find a route between these locations")
                st.stop()
            
            # Step 4: Extract towns along the route
            st.info("Step 4: Extracting towns along the route...")
            waypoints = route_service.extract_towns_from_route(route_data.get("geometry", {}))
            
            # Step 5: Generate intelligent search queries
            st.info("Step 5: Generating search queries with AI...")
            search_queries = ai_service.generate_search_queries(source, destination, search_query)
            
            # ==================== Display Results ====================
            st.success("✅ Route analysis complete!")
            
            # Route Summary
            st.markdown("### 📊 Route Summary")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                distance = route_data.get("distance", 0)
                st.metric("Distance", format_distance(distance))
            
            with col2:
                duration = route_data.get("duration", 0)
                st.metric("Duration", format_duration(duration))
            
            with col3:
                st.metric("Waypoints", len(waypoints))
            
            # Route Details
            st.markdown("### 📍 Location Details")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**From:** {source_data['full_name']}")
                st.write(f"Coordinates: {source_data['latitude']:.4f}, {source_data['longitude']:.4f}")
            
            with col2:
                st.write(f"**To:** {dest_data['full_name']}")
                st.write(f"Coordinates: {dest_data['latitude']:.4f}, {dest_data['longitude']:.4f}")
            
            # AI Generated Search Queries
            st.markdown("### 🤖 AI-Generated Search Queries")
            for i, query in enumerate(search_queries, 1):
                st.write(f"{i}. {query}")
            
            # Search Results
            st.markdown("### 🏪 Search Results")
            st.info("**MVP Version:** Displaying sample results. Real search integration coming soon!")
            
            # Show results for each waypoint
            for idx, waypoint in enumerate(waypoints[:3], 1):  # Show first 3 waypoints
                with st.expander(f"📍 Waypoint {idx} Results"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Latitude:** {waypoint['latitude']:.4f}")
                        st.write(f"**Longitude:** {waypoint['longitude']:.4f}")
                    
                    with col2:
                        # Run searches for each query at this waypoint
                        for query in search_queries[:2]:  # Show 2 queries per waypoint
                            results = search_service.search_places(query, f"Waypoint {idx}")
                            if results:
                                st.write(f"**{query}:**")
                                for result in results:
                                    st.write(f"- {result['name']} (Rating: ⭐ {result['rating']})")

# ==================== Sidebar Info ====================
st.sidebar.markdown("### ℹ️ About")
st.sidebar.markdown("""
**AI Route Explorer** helps you find businesses and places along your journey.

**Features:**
- 🗺️ Route optimization
- 🤖 AI-powered query generation
- 🏪 Business discovery
- 📍 Location extraction

**Tech Stack:**
- Streamlit (Frontend)
- OpenRouteService API (Routing)
- Ollama (AI)
- Python (Backend)

**Note:** MVP version with placeholder search. Production version will include real APIs.
""")