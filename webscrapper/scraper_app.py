"""
Web Scraper App - Find businesses/places with simple search
No route/location parameters needed - just search!
"""

import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from datetime import datetime
import time

# ==================== Logging Setup ====================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== Page Configuration ====================
st.set_page_config(
    page_title="Web Scraper - Find Anything",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
<style>
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    .result-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px;
        border-radius: 8px;
        color: white;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== Header ====================
st.title("🔍 Web Scraper - Find Anything Online")
st.markdown("**Simple, Fast, No Location Needed!** - Just search and get results")

# ==================== Sidebar Settings ====================
with st.sidebar:
    st.header("⚙️ Settings")
    search_type = st.radio(
        "What do you want to search?",
        ["📍 Businesses/Places", "🏢 Companies", "📰 News", "🛍️ Products"]
    )
    
    results_limit = st.slider("Number of results", 5, 20, 10)
    include_links = st.checkbox("Include website links", value=True)
    
    st.markdown("---")
    st.markdown("**📊 How it works:**")
    st.markdown("""
    1. Enter your search query
    2. Select result type
    3. Get instant results
    4. No API keys needed!
    """)

# ==================== Main App ====================
st.markdown("---")

# Search input
search_query = st.text_input(
    "🔎 Search for anything:",
    placeholder="e.g., 'restaurants in Karachi', 'apple stores', 'pizza delivery'",
    label_visibility="collapsed"
)

col1, col2, col3 = st.columns([2, 1, 1])

with col2:
    search_button = st.button("🔍 Search", use_container_width=True)

with col3:
    clear_button = st.button("🗑️ Clear", use_container_width=True)

# ==================== Search Functions ====================

def search_google(query, num_results=10):
    """Search Google and scrape results"""
    try:
        logger.info(f"Searching Google for: {query}")
        
        # Google search URL
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        results = []
        search_results = soup.find_all('div', class_='g')
        
        for result in search_results[:num_results]:
            try:
                title_elem = result.find('h3')
                link_elem = result.find('a')
                desc_elem = result.find('span', class_='st')
                
                if title_elem and link_elem:
                    title = title_elem.text.strip()
                    link = link_elem.get('href', '#')
                    description = desc_elem.text.strip() if desc_elem else "No description"
                    
                    if link.startswith('http'):
                        results.append({
                            'Title': title,
                            'URL': link,
                            'Description': description[:150] + "..." if len(description) > 150 else description
                        })
            except Exception as e:
                logger.debug(f"Error parsing result: {e}")
                continue
        
        return results
    
    except Exception as e:
        logger.error(f"Google search error: {e}")
        return []


def search_wikipedia(query, num_results=5):
    """Search Wikipedia"""
    try:
        logger.info(f"Searching Wikipedia for: {query}")
        
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            'action': 'query',
            'list': 'search',
            'srsearch': query,
            'format': 'json',
            'srlimit': num_results
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        results = []
        for item in data.get('query', {}).get('search', []):
            results.append({
                'Title': item['title'],
                'URL': f"https://en.wikipedia.org/wiki/{item['title'].replace(' ', '_')}",
                'Description': item['snippet'][:150] + "..." if len(item['snippet']) > 150 else item['snippet']
            })
        
        return results
    
    except Exception as e:
        logger.error(f"Wikipedia search error: {e}")
        return []


def scrape_business_listings(query):
    """Scrape business directories"""
    try:
        logger.info(f"Scraping business listings for: {query}")
        
        # Using DuckDuckGo as alternative (more reliable)
        url = f"https://duckduckgo.com/?q={query.replace(' ', '+')}&t=h_&ia=web"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        results = []
        # DuckDuckGo results
        for result in soup.find_all('div', class_='result'):
            try:
                title = result.find('a', class_='result__a')
                if title:
                    results.append({
                        'Title': title.text.strip(),
                        'URL': title.get('href', '#'),
                        'Description': result.find('a', class_='result__snippet').text if result.find('a', class_='result__snippet') else 'No description'
                    })
            except:
                continue
        
        return results[:results_limit]
    
    except Exception as e:
        logger.error(f"Business scraping error: {e}")
        return []


# ==================== Display Results ====================
if search_button and search_query:
    with st.spinner("🔍 Searching and scraping..."):
        time.sleep(1)  # Small delay to avoid blocking
        
        logger.info(f"User search: {search_query}")
        
        # Get results based on search type
        if search_type == "📍 Businesses/Places":
            results = scrape_business_listings(search_query)
            source = "DuckDuckGo"
        elif search_type == "🛍️ Products":
            results = search_google(search_query, results_limit)
            source = "Google"
        else:
            results = search_google(search_query, results_limit)
            source = "Google"
        
        # Add Wikipedia results as bonus
        wiki_results = search_wikipedia(search_query, 3)
        
        if results or wiki_results:
            st.success(f"✅ Found results!")
            
            # Create tabs
            tab1, tab2, tab3 = st.tabs(["Main Results", "Wikipedia", "Export Data"])
            
            with tab1:
                if results:
                    st.subheader(f"📊 {len(results)} Results from {source}")
                    
                    for idx, result in enumerate(results, 1):
                        with st.container():
                            col1, col2 = st.columns([4, 1])
                            
                            with col1:
                                st.markdown(f"### {idx}. {result['Title']}")
                                st.markdown(f"**Description:** {result['Description']}")
                                
                                if include_links and result['URL'] != '#':
                                    st.markdown(f"🔗 [Visit Link]({result['URL']})")
                            
                            with col2:
                                st.metric("Result", f"#{idx}")
                            
                            st.divider()
                else:
                    st.warning("⚠️ No results found. Try a different search term.")
            
            with tab2:
                if wiki_results:
                    st.subheader("📚 Wikipedia Results")
                    for idx, result in enumerate(wiki_results, 1):
                        st.markdown(f"### {idx}. {result['Title']}")
                        st.markdown(f"{result['Description']}")
                        st.markdown(f"🔗 [Read More]({result['URL']})")
                        st.divider()
                else:
                    st.info("No Wikipedia results found.")
            
            with tab3:
                if results:
                    df = pd.DataFrame(results)
                    st.dataframe(df, use_container_width=True)
                    
                    # Download as CSV
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download as CSV",
                        data=csv,
                        file_name=f"search_results_{search_query.replace(' ', '_')}.csv",
                        mime="text/csv"
                    )
                    
                    # Download as JSON
                    import json
                    json_data = json.dumps(results, indent=2)
                    st.download_button(
                        label="📥 Download as JSON",
                        data=json_data,
                        file_name=f"search_results_{search_query.replace(' ', '_')}.json",
                        mime="application/json"
                    )
        else:
            st.error("❌ No results found. Please try a different search.")

elif clear_button:
    st.rerun()

# ==================== Footer ====================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px;'>
    <p>🚀 Web Scraper App | Free & Simple Search Tool</p>
    <p>Powered by Streamlit | No API Keys Required</p>
</div>
""", unsafe_allow_html=True)
