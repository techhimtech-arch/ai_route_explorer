# 🗺️ AI Route Explorer

An AI-powered web app that helps you find businesses and places along your route.

## Features

✅ **Route Finding** - Get optimal routes between locations using OpenRouteService API
✅ **AI Query Generation** - Intelligent search queries using Ollama local AI
✅ **Business Discovery** - Find places/businesses along your route
✅ **Clean UI** - Built with Streamlit for easy usage
✅ **Modular Architecture** - Clean separation of concerns

## Project Structure

```
route-explorer/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
│
├── services/                   # Business logic modules
│   ├── __init__.py
│   ├── route_service.py       # OpenRouteService API integration
│   ├── ai_service.py          # Ollama AI integration
│   └── search_service.py      # Search functionality
│
├── utils/                      # Helper utilities
│   ├── __init__.py
│   └── helpers.py             # Formatting and validation functions
│
└── data/                       # Data storage (for later)
```

## Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **Routing:** OpenRouteService API
- **AI:** Ollama (local LLM)
- **Search:** Tavily API (to be integrated)
- **Web Scraping:** Playwright (future)

## Prerequisites

- Python 3.8+
- Ollama installed and running (for AI features)
  - Download: https://ollama.ai
  - Run: `ollama serve`
  - Pull a model: `ollama pull mistral`
- OpenRouteService API key (free tier available)

## Installation

### 1. Clone/Setup Project

```bash
cd route-explorer
```

### 2. Create Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables (Optional)

Create a `.env` file:
```
OPENROUTE_API_KEY=your_api_key_here
OLLAMA_URL=http://localhost:11434
```

## Running the App

```bash
streamlit run app.py
```

The app will open at: `http://localhost:8501`

## MVP Features Currently Working

1. **Route Finding** ✅
   - Geocodes source and destination locations
   - Calculates optimal route between them
   - Shows distance and duration

2. **Town Extraction** ✅
   - Extracts waypoints along the route
   - Basic implementation (can be enhanced)

3. **AI Query Generation** ✅
   - Generates search queries using Ollama
   - Falls back to simple queries if Ollama unavailable

4. **Search Results** 🔄
   - UI ready for displaying results
   - Placeholder results in MVP
   - Ready for real API integration

## Build Roadmap

### Phase 1: MVP (Current)
- [x] Route fetching from OpenRouteService
- [x] Location geocoding
- [x] Waypoint extraction
- [x] AI query generation
- [ ] Real search integration

### Phase 2: Search Integration
- [ ] Integrate Tavily API for web search
- [ ] Add Google Places API
- [ ] Implement Playwright for scraping
- [ ] Cache search results

### Phase 3: Enhancement
- [ ] Map visualization
- [ ] Favorites/bookmarks
- [ ] Review aggregation
- [ ] Route filtering options

### Phase 4: Production
- [ ] Database for storing searches
- [ ] User authentication
- [ ] Search history
- [ ] Advanced filtering

## API Configuration

### OpenRouteService

1. Get free API key: https://openrouteservice.org
2. Update `API_KEY` in `app.py`
3. Free tier: 40 requests/minute, 1750/day

### Ollama Setup

```bash
# Install Ollama from https://ollama.ai

# Start Ollama service
ollama serve

# In another terminal, pull a model (one-time)
ollama pull mistral
# or
ollama pull neural-chat
ollama pull dolphin-mixtral
```

## Usage Example

1. Open the app
2. Enter:
   - **From:** Shimla
   - **To:** Paonta Sahib
   - **What to find:** plant nurseries
3. Click "Search Route & Places"
4. Get results with route info and search queries

## Code Structure Explanation

### RouteService (`services/route_service.py`)
- Handles all OpenRouteService API calls
- Methods:
  - `geocode_location()` - Convert place name to coordinates
  - `get_route()` - Get route between two points
  - `extract_towns_from_route()` - Extract waypoints

### AIService (`services/ai_service.py`)
- Integrates with Ollama local AI
- Methods:
  - `generate_search_queries()` - Generate smart queries
  - `check_ollama_connection()` - Verify Ollama is running

### SearchService (`services/search_service.py`)
- Handles business/place search
- Methods:
  - `search_places()` - Search at specific location
  - `search_multiple_queries()` - Multi-query search
- **MVP:** Returns placeholder results
- **TODO:** Integrate real search APIs

### Utils (`utils/helpers.py`)
- Helper functions:
  - `format_distance()` - Format meters to km/m
  - `format_duration()` - Format seconds to hours:minutes
  - `validate_coordinates()` - Validate lat/lon

## Common Issues & Solutions

### Issue: "Ollama connection refused"
**Solution:** 
```bash
ollama serve
# Keep this running while using the app
```

### Issue: "API key is invalid"
**Solution:**
1. Get new key from https://openrouteservice.org
2. Update `API_KEY` in `app.py`

### Issue: "Location not found"
**Solution:**
- Try full address instead of just city name
- Use country/state names if ambiguous

## Contributing

To extend the app:

1. Add new services in `services/` folder
2. Add utilities in `utils/` folder
3. Update main `app.py` to use new features
4. Test with `streamlit run app.py`

## Future Enhancements

- [ ] Map visualization with route overlay
- [ ] Real-time traffic updates
- [ ] User reviews aggregation
- [ ] Image gallery for places
- [ ] Directions integration
- [ ] ETA calculations
- [ ] Multi-stop routing
- [ ] Saved routes & favorites

## Performance Tips

- Cache API responses
- Batch search queries
- Use local Ollama instead of cloud AI
- Limit waypoints for large routes

## License

MIT - Feel free to use and modify

## Support

For issues or questions:
1. Check the error messages in Streamlit UI
2. Verify API key validity
3. Ensure Ollama is running
4. Check internet connection

---

**Built with ❤️ for exploring routes smartly!**
