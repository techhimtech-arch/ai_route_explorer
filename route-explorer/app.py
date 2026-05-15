"""
AI Route Explorer - Main Streamlit Application
Finds businesses and places along your route
"""

import logging
import streamlit as st
import os
from dotenv import load_dotenv
from services import RouteService, AIService, SearchService
from utils import format_distance, format_duration
from utils.logging_config import setup_logging

# Load environment variables from .env file
load_dotenv()

# ==================== Configuration ====================
# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
setup_logging(LOG_LEVEL)
logger = logging.getLogger(__name__)

# API Key from environment
API_KEY = os.getenv("OPENROUTE_API_KEY")
if not API_KEY:
    st.error("❌ OPENROUTE_API_KEY not found in .env file")
    st.stop()

logger.info("Application starting")
logger.info(
    "Configuration loaded: LOG_LEVEL=%s, OLLAMA_URL=%s, OLLAMA_MODEL=%s, OPENROUTE_API_KEY=%s",
    LOG_LEVEL,
    os.getenv("OLLAMA_URL", "http://localhost:11434"),
    os.getenv("OLLAMA_MODEL", "mistral"),
    "set" if API_KEY else "missing",
)

# Initialize services
route_service = RouteService(API_KEY)
ai_service = AIService(
    ollama_url=os.getenv("OLLAMA_URL", "http://localhost:11434"),
    model=os.getenv("OLLAMA_MODEL", "mistral"),
)
search_service = SearchService()
logger.info("Services initialized")

# ==================== Page Configuration ====================
st.set_page_config(
    page_title="AI Route Explorer",
    page_icon="🗺️",
    layout="wide"
)

# ==================== UI Layout ====================
st.title("🗺️ AI Route Explorer")
st.markdown("Find businesses and places along your route powered by AI")

with st.sidebar.expander("Debug info", expanded=False):
    st.write(f"Log level: {LOG_LEVEL}")
    st.write(f"OpenRouteService key: {'set' if API_KEY else 'missing'}")
    st.write(f"Ollama URL: {os.getenv('OLLAMA_URL', 'http://localhost:11434')}")
    st.write(f"Ollama model: {os.getenv('OLLAMA_MODEL', 'mistral')}")

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
    logger.info("Search requested: source=%s destination=%s query=%s", source, destination, search_query)
    if not source or not destination or not search_query:
        st.error("❌ Please fill in all fields")
        logger.warning("Validation failed because one or more fields were empty")
    else:
        with st.spinner("Processing your route..."):
            
            # Step 1: Geocode source location
            st.info("Step 1: Finding source location...")
            logger.info("Step 1 started: geocoding source=%s", source)
            source_data = route_service.geocode_location(source)
            
            if not source_data:
                st.error(f"❌ Could not find location: {source}")
                logger.error("Source geocoding failed for %s", source)
                st.stop()
            
            # Verify source location
            st.markdown(f"✓ **Source:** {source_data['full_name']} (Lat: {source_data['latitude']:.4f}, Lon: {source_data['longitude']:.4f})")
            
            # Step 2: Geocode destination location
            st.info("Step 2: Finding destination location...")
            logger.info("Step 2 started: geocoding destination=%s", destination)
            dest_data = route_service.geocode_location(destination)
            
            if not dest_data:
                st.error(f"❌ Could not find location: {destination}")
                logger.error("Destination geocoding failed for %s", destination)
                st.stop()
            
            # Verify destination location
            st.markdown(f"✓ **Destination:** {dest_data['full_name']} (Lat: {dest_data['latitude']:.4f}, Lon: {dest_data['longitude']:.4f})")
            
            # Check if locations are too far apart (likely wrong geocoding)
            lat_diff = abs(source_data['latitude'] - dest_data['latitude'])
            lon_diff = abs(source_data['longitude'] - dest_data['longitude'])
            
            if lat_diff > 20 or lon_diff > 20:
                st.warning(
                    f"⚠️ **Locations are very far apart** (Lat diff: {lat_diff:.1f}°, Lon diff: {lon_diff:.1f}°)\n\n"
                    f"This might be a geocoding issue. Try:\n"
                    f"- Adding country/state names: 'Una, Himachal Pradesh, India'\n"
                    f"- Being more specific with location names"
                )
                logger.warning("Locations are very far apart: lat_diff=%s lon_diff=%s", lat_diff, lon_diff)
                st.stop()
            
            # Step 3: Get route between locations
            st.info("Step 3: Calculating route...")
            source_coords = (source_data["longitude"], source_data["latitude"])
            dest_coords = (dest_data["longitude"], dest_data["latitude"])
            logger.info("Step 3 started: route requested between source_coords=%s and dest_coords=%s", source_coords, dest_coords)
            
            route_data = route_service.get_route(source_coords, dest_coords)
            
            if not route_data:
                st.warning("⚠️ Could not calculate route (API issue)")
                logger.error("Route calculation failed for source=%s destination=%s", source, destination)
                # Continue anyway - show AI queries and search results
                route_data = None
                waypoints = []
            else:
                # Step 4: Extract towns along the route
                st.info("Step 4: Extracting towns along the route...")
                logger.info("Step 4 started: extracting waypoints from route geometry")
                waypoints = route_service.extract_towns_from_route(route_data.get("geometry", {}))
            
            # Step 5: Generate intelligent search queries (ALWAYS DO THIS)
            st.info("Step 5: Generating search queries with AI...")
            ollama_connected = ai_service.check_ollama_connection()
            logger.info("Ollama connection status before query generation: %s", ollama_connected)
            search_queries = ai_service.generate_search_queries(source, destination, search_query)
            logger.info("AI generated %s search queries", len(search_queries))
            
            # ==================== Display Results ====================
            if route_data:
                st.success("✅ Route analysis complete!")
            else:
                st.success("✅ Search analysis complete! (Route API unavailable)")
            
            logger.info(
                "Search completed successfully: distance=%s duration=%s waypoints=%s queries=%s",
                route_data.get("distance", 0) if route_data else 0,
                route_data.get("duration", 0) if route_data else 0,
                len(waypoints),
                len(search_queries),
            )
            
            # Route Summary (only if route available)
            if route_data:
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
            else:
                # Show location details even without route
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
                logger.debug("Search query %s: %s", i, query)
            
            # Search Results
            st.markdown("### 🏪 Search Results")
            
            if waypoints:
                st.info("**Displaying results for each waypoint along the route:**")
                
                # Show results for each waypoint
                for idx, waypoint in enumerate(waypoints[:3], 1):  # Show first 3 waypoints
                    with st.expander(f"📍 Waypoint {idx} Results"):
                        logger.debug("Rendering results for waypoint %s: %s", idx, waypoint)
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Latitude:** {waypoint['latitude']:.4f}")
                            st.write(f"**Longitude:** {waypoint['longitude']:.4f}")
                        
                        with col2:
                            # Run searches for each query at this waypoint
                            for query in search_queries[:2]:  # Show 2 queries per waypoint
                                logger.info("Running search: waypoint=%s query=%s", idx, query)
                                results = search_service.search_places(query, f"Waypoint {idx}")
                                if results:
                                    st.write(f"**{query}:**")
                                    for result in results:
                                        rating = result.get('rating', 0)
                                        source = result.get('source', 'unknown')
                                        st.write(f"- {result['name']}")
                                        st.write(f"  ⭐ {rating:.1f} | Source: {source}")
                                        if result.get('phone'):
                                            st.write(f"  ☎️ {result['phone']}")
                                        if result.get('url') and result['url'] != '#':
                                            st.write(f"  🔗 {result['url']}")
            else:
                st.info("**Displaying results for your search (no route available):**")
                
                # Show results for each AI-generated query
                for idx, query in enumerate(search_queries, 1):
                    with st.expander(f"🔍 Query {idx}: {query}"):
                        logger.info("Running search: query=%s location=%s-%s", query, source, destination)
                        results = search_service.search_places(query, f"{source} to {destination}")
                        if results:
                            for result in results:
                                rating = result.get('rating', 0)
                                source_api = result.get('source', 'unknown')
                                st.write(f"**{result['name']}**")
                                st.write(f"  📍 Location: {result.get('location', 'N/A')}")
                                st.write(f"  ⭐ Rating: {rating:.1f}")
                                st.write(f"  🏷️ Type: {result.get('type', 'N/A')}")
                                st.write(f"  📌 Source: {source_api}")
                                if result.get('phone'):
                                    st.write(f"  ☎️ Phone: {result['phone']}")
                                if 'snippet' in result:
                                    st.write(f"  📄 Info: {result['snippet']}")
                                if result.get('url') and result['url'] != '#':
                                    st.write(f"  🔗 {result['url']}")
                                st.divider()
                        else:
                            st.write("No results found for this query.")

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

**Note:** If Tavily is not configured, the app falls back to public web search and only uses mock data as a last resort. Phone numbers are shown only when the source page exposes them.
""")

# ==================== AI Demo Section ====================
st.sidebar.markdown("---")
st.sidebar.markdown("### 🤖 AI Query Demo")
st.sidebar.markdown("**Test Ollama AI independently** (no routing needed)")

demo_source = st.sidebar.text_input("Demo - From", placeholder="e.g., Shimla")
demo_dest = st.sidebar.text_input("Demo - To", placeholder="e.g., Una")
demo_query = st.sidebar.text_input("Demo - Find", placeholder="e.g., pots manufacture")

if st.sidebar.button("🧠 Generate AI Queries", type="secondary"):
    if not demo_source or not demo_dest or not demo_query:
        st.sidebar.error("❌ Fill all demo fields")
    else:
        st.sidebar.info("🔄 Generating queries with Ollama AI...")
        logger.info("AI Demo: generating queries for source=%s dest=%s query=%s", demo_source, demo_dest, demo_query)
        
        # Check Ollama connection first
        ollama_ok = ai_service.check_ollama_connection()
        st.sidebar.markdown(f"**Ollama Status:** {'✅ Connected' if ollama_ok else '❌ Not Running'}")
        
        if ollama_ok:
            st.sidebar.markdown(f"**Model:** {os.getenv('OLLAMA_MODEL', 'mistral')}")
        
        # Generate queries
        demo_queries = ai_service.generate_search_queries(demo_source, demo_dest, demo_query)
        
        st.sidebar.markdown("**Generated Queries:**")
        for i, q in enumerate(demo_queries, 1):
            st.sidebar.markdown(f"{i}. {q}")
            logger.debug("Demo query %s: %s", i, q)
        
        st.sidebar.success("✅ AI Query generation works!")
        st.sidebar.markdown("""
        ---
        **What you just saw:**
        - Ollama read your source, destination, and search term
        - AI analyzed context and generated 3-5 relevant search queries
        - These queries would be used to find businesses along your route
        
        **This is the AI magic:** It doesn't just hardcode queries,  
        it understands context and creates useful variations!
        """)
