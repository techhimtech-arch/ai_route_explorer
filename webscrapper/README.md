# 🎓 School Digital Gap Scanner

An AI-powered lead generation tool that identifies schools with poor or missing digital presence and generates high-quality business leads for website development services.

## Overview

The School Digital Gap Scanner automatically discovers schools in your target locations, analyzes their digital presence, and generates actionable business leads. Perfect for:
- Web development agencies
- Digital marketing firms
- SEO service providers
- IT consulting firms
- Schools looking to benchmark competition

## 🎯 Core Features

### 1. **School Discovery**
- Search schools by city and state
- Multiple data sources (directories, public listings)
- Scalable to any location
- Configurable search limits

### 2. **Website Analysis**
Detects:
- ❌ **Missing websites** - Critical digital gap
- 🔗 **Broken/inaccessible websites** - Poor user experience
- 🔒 **No SSL certificate** - Security risk
- 📱 **Not mobile-friendly** - Limits mobile user access (60%+)
- 📅 **Outdated design** - Poor perception
- 📧 **Missing contact info** - Lost leads
- 📢 **No social presence** - Limited engagement

### 3. **Digital Quality Score**
- **0-100 scale** with letter grades (A-F)
- Component breakdown for detailed insights
- Identifies specific digital gaps
- Suggests targeted improvements

### 4. **Lead Generation**
- Automatic lead prioritization (HOT/WARM/COOL)
- Sales-ready CSV export
- Business opportunity assessment
- Revenue potential estimation

### 5. **Export & Reporting**
- Complete school analysis (CSV)
- High-priority leads list
- Summary reports with statistics
- Download-ready formats

## 📊 Scoring Breakdown

| Grade | Score | Assessment |
|-------|-------|------------|
| A | 85-100 | Modern, well-designed website |
| B | 75-84 | Good website with minor issues |
| C | 65-74 | Functional but outdated |
| D | 50-64 | Poor digital presence |
| F | <50 | Critical digital gaps |

## 🏗️ Project Structure

```
project/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
│
├── scrapers/                       # School discovery & analysis
│   ├── __init__.py
│   ├── school_scraper.py          # School discovery from multiple sources
│   └── website_analyzer.py        # Website quality analysis
│
├── services/                       # Business logic
│   ├── __init__.py
│   ├── scoring_service.py         # Digital quality scoring
│   └── export_service.py          # CSV/report export
│
├── utils/                          # Utilities & helpers
│   ├── __init__.py
│   ├── helpers.py                 # Helper functions
│   └── logging_config.py          # Logging setup
│
├── data/                           # Cached data
├── exports/                        # Generated exports (CSV, reports)
├── logs/                           # Application logs
│
├── README.md                       # This file
└── docs/                           # Additional documentation
```

## 🚀 Quick Start

### 1. **Installation**

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# On Windows, install Playwright browsers:
python -m playwright install
```

### 2. **Configuration**

Create `.env` file (copy from `.env.example`):

```env
LOG_LEVEL=INFO
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=mistral
```

### 3. **Run the Application**

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📖 Usage Guide

### Basic Scan

1. **Enter Search Location**
   - City: e.g., "New York"
   - State: e.g., "NY"

2. **Configure Scan Settings**
   - Number of schools to scan (5-100)
   - Website timeout (5-30 seconds)
   - Rate limit delay (0.5-3 seconds)
   - Optional: Check SSL, Mobile Friendly, Broken Links

3. **Start Scanning**
   - Click "🔍 Start Scanning"
   - Monitor progress in real-time

4. **Review Results**
   - View all schools in table format
   - Identify hot leads (priority opportunities)
   - Review statistics and gaps
   - Export data for follow-up

### Export Options

**All Schools CSV**
- Complete analysis of every school
- Digital scores and grades
- Technical details (SSL, mobile, etc.)
- Key issues identified

**Leads Only CSV**
- High-priority opportunities only
- Sales-ready format
- Recommended services
- Opportunity assessment

**Summary Report**
- Location statistics
- Market opportunity analysis
- Gap distribution
- Revenue potential

## 🔧 Advanced Configuration

### Scan Settings

| Setting | Range | Default | Purpose |
|---------|-------|---------|---------|
| Schools to scan | 5-100 | 20 | Number of schools to analyze |
| Website timeout | 5-30s | 10s | Max time to wait per website |
| Rate limit delay | 0.5-3s | 1.0s | Delay between requests (respectful scraping) |
| Check SSL | Yes/No | Yes | Verify SSL certificates |
| Check Mobile | Yes/No | Yes | Test mobile responsiveness |
| Check Links | Yes/No | No | Test internal links (slower) |

### Performance Tips

- **Reduce timeout** for faster scans (but may miss sites)
- **Decrease rate limit** for faster scans (but risk IP blocks)
- **Increase school limit** for more comprehensive data
- **Disable link checking** for faster scans (rarely affects score)

## 📊 Output Examples

### School Analysis Table

| School | Website | Status | Score | Grade | Gap Type |
|--------|---------|--------|-------|-------|----------|
| Lincoln High | No Website | No Digital Presence | 5.0 | F | No Website |
| Kennedy Prep | example.edu | Not Mobile Friendly | 55.0 | D | Mobile Gap |
| Roosevelt MS | example-school.org | Modern Website | 92.0 | A | - |

### Lead List (Sales-Ready)

| School | Current Website | Opportunity | Priority | Score | Services |
|--------|-----------------|-------------|----------|-------|----------|
| Lincoln High | No Website | No Digital Presence | HOT 🔥 | 5.0 | Website Design, SEO |
| Adams School | broken-link.edu | Broken Website | HOT 🔥 | 12.0 | Website Repair |

### Summary Report

```
╔═══════════════════════════════════════════════════════════════════╗
║           SCHOOL DIGITAL GAP ANALYSIS REPORT                      ║
╚═══════════════════════════════════════════════════════════════════╝

Report Generated: 2024-01-15 14:30:00
Location: New York, NY

📊 OVERVIEW
─────────────────────────────────────────────────────────────────
Total Schools Analyzed: 50
Average Digital Score: 42.3/100
Sales Leads Identified: 28

💼 BUSINESS OPPORTUNITY
─────────────────────────────────────────────────────────────────
HIGH-PRIORITY LEADS: 28 schools

Potential Revenue: $84,000 - $420,000
```

## 🔍 Detection Methods

### No Website Detection
- DNS lookup failure
- Connection timeout
- 404/503 responses

### SSL Certificate Check
- Validates certificate chain
- Checks certificate expiration
- Verifies domain match

### Mobile Friendliness
- Checks for viewport meta tag
- Analyzes responsive design indicators
- Tests touch-friendly elements

### Outdated Design
- Analyzes HTML structure
- Detects old layout patterns (tables, frames)
- Identifies deprecated HTML tags

### Broken Links
- Tests sample internal links
- Checks HTTP response codes
- Reports redirect chains

## 🤝 Contributing

Want to improve the scanner? Here's how:

### Add New Data Source
1. Create method in `SchoolScraper`
2. Implement data parsing
3. Map to standard school schema
4. Add tests

### Enhance Analysis
1. Add detection method to `WebsiteAnalyzer`
2. Update scoring in `ScoringService`
3. Document findings
4. Test edge cases

### Improve UI
1. Edit `app.py` Streamlit components
2. Add visualizations
3. Improve export formats
4. Test user flow

## 📝 API Reference

### SchoolScraper

```python
scraper = SchoolScraper(rate_limit_delay=1.0)
schools = scraper.search_schools_by_city_state("New York", "NY", limit=50)
```

### WebsiteAnalyzer

```python
analyzer = WebsiteAnalyzer(timeout=10)
analysis = analyzer.analyze("https://example.edu")
# Returns: {
#   'has_website': True,
#   'has_ssl': True,
#   'is_mobile_friendly': True,
#   'has_contact': True,
#   'has_social': True,
#   'html_age_indicator': 'modern',
#   ...
# }
```

### ScoringService

```python
scorer = ScoringService()
score = scorer.calculate_score(school, analysis)
# Returns: {
#   'total_score': 85.5,
#   'grade': 'A',
#   'gap_type': 'Opportunity for Enhancement',
#   'key_issues': [...],
#   'recommendations': [...]
# }
```

### ExportService

```python
exporter = ExportService(export_dir='exports')
filepath = exporter.export_to_csv(scores)
filepath = exporter.export_to_leads_csv(scores)
filepath = exporter.export_summary_report(scores, city, state)
```

## ⚠️ Important Notes

### Ethical Scraping

- **Rate limiting**: Built-in 1-2 second delays between requests
- **User-Agent**: Identifies as legitimate browser
- **No aggressive scraping**: Respects robots.txt
- **Public data only**: Uses only publicly available information

### Legal Compliance

- ✅ Scrapes public school directories
- ✅ Analyzes public websites
- ✅ Uses educational data sources
- ❌ Does not scrape login-protected content
- ❌ Does not overload servers

### Data Privacy

- Data is stored locally only
- No personal information collected
- No student/staff data accessed
- Compliant with FERPA

## 🐛 Troubleshooting

### "No schools found"

**Issue**: Search returns empty results
**Solution**: 
- Verify city/state spelling
- Try larger radius or nearby cities
- Check internet connection
- Review logs for errors

### "Website analysis timeout"

**Issue**: Scan takes too long
**Solution**:
- Reduce timeout setting (8-10 seconds)
- Reduce schools to scan limit
- Disable link checking
- Check network speed

### "Export file not found"

**Issue**: CSV/report not downloading
**Solution**:
- Check `exports/` directory permissions
- Verify disk space available
- Try different export format
- Review error logs

### "High error rate during scan"

**Issue**: Many websites fail to analyze
**Solution**:
- Increase timeout slightly
- Reduce rate limit (slower but more reliable)
- Check IP block status (VPN may help)
- Verify internet connectivity

## 📞 Support

For questions, issues, or feature requests:

1. Check the docs/ directory
2. Review logs in logs/ directory
3. Check GitHub issues (if applicable)
4. Contact support team

## 📄 License

[Your License Here]

## 🎓 Educational Use

This tool was designed to demonstrate:
- Web scraping best practices
- Data analysis workflows
- Streamlit application development
- Business intelligence tools
- Python service architecture

## 🔄 Version History

**v1.0** (Initial Release)
- School discovery
- Website analysis
- Digital quality scoring
- Lead generation
- CSV export
- Streamlit UI

## 🚀 Roadmap

**Future Features**:
- [ ] API integration for bulk scanning
- [ ] Email notification for new leads
- [ ] CRM integration (HubSpot, Salesforce)
- [ ] Advanced analytics dashboard
- [ ] Competitor analysis
- [ ] AI-powered recommendations
- [ ] Automated outreach templates
- [ ] Lead scoring refinement

---

**Built with ❤️ for school digital transformation**
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
