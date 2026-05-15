"""
Search Service - Handles web search for finding businesses and places
"""

import logging
import os
import re
from typing import List, Dict, Optional
import requests


logger = logging.getLogger(__name__)

class SearchService:
    """
    Service for searching businesses and places along the route
    Uses Google Places or Tavily for real results, with web fallback and mock as last resort
    """
    
    def __init__(self):
        """
        Initialize SearchService with optional search API keys
        """
        self.google_places_key = os.getenv("GOOGLE_PLACES_API_KEY", "")
        self.tavily_key = os.getenv("TAVILY_API_KEY", "")
        self.tavily_url = "https://api.tavily.com/search"

        if self.google_places_key:
            logger.info("SearchService initialized with Google Places API")
        
        if self.tavily_key:
            logger.info("SearchService initialized with Tavily API")
        elif not self.google_places_key:
            logger.warning("SearchService: No Google Places or Tavily API key found. Using fallback results.")
        
    def search_places(self, query: str, location: str) -> List[Dict]:
        """
        Search for places/businesses matching the query
        
        Args:
            query: Search query (e.g., "plant nurseries")
            location: Location to search in (or "Waypoint X")
            
        Returns:
            List of search results
        """
        try:
            logger.info("Searching places with query=%s location=%s", query, location)
            
            # Prefer Google Places for business data like name, address, and phone
            if self.google_places_key:
                return self._search_with_google_places(query, location)

            # If Tavily API key is available, use real web search
            if self.tavily_key:
                return self._search_with_tavily(query, location)
            else:
                logger.info("Tavily API key not configured. Trying public web search fallback.")
                fallback_results = self._search_with_duckduckgo(query, location)
                if fallback_results:
                    return fallback_results

                logger.info("Public web search fallback returned no results. Using mock results.")
                return self._mock_results(query, location)
            
        except Exception as e:
            logger.exception("Error searching places")
            return []

    def _search_with_google_places(self, query: str, location: str) -> List[Dict]:
        """
        Search using Google Places Text Search + Place Details.

        Args:
            query: Search query
            location: Location context

        Returns:
            List of place results with contact data when available
        """
        try:
            search_query = f"{query} in {location}"
            logger.info("Executing Google Places search: query=%s", search_query)

            text_search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
            response = requests.get(
                text_search_url,
                params={
                    "query": search_query,
                    "key": self.google_places_key,
                },
                timeout=10,
            )
            response.raise_for_status()

            data = response.json()
            api_status = data.get("status")
            if api_status not in ("OK", "ZERO_RESULTS"):
                logger.warning("Google Places text search returned status=%s error=%s", api_status, data.get("error_message"))

            results: List[Dict] = []
            for item in data.get("results", [])[:5]:
                place_id = item.get("place_id")
                details = self._get_google_place_details(place_id) if place_id else {}

                phone = details.get("formatted_phone_number") or details.get("international_phone_number")
                website = details.get("website") or item.get("website")
                address = details.get("formatted_address") or item.get("formatted_address")

                results.append({
                    "name": item.get("name", "Unknown"),
                    "location": address or location,
                    "type": query,
                    "rating": item.get("rating", 0),
                    "source": "google_places",
                    "url": website or f"https://www.google.com/maps/search/?api=1&query={requests.utils.quote(item.get('name', query))}",
                    "snippet": item.get("formatted_address", ""),
                    "phone": phone,
                })

            logger.info("Google Places returned %s result(s)", len(results))
            return results

        except Exception:
            logger.exception("Google Places search failed, falling back to Tavily/web/mock")
            if self.tavily_key:
                return self._search_with_tavily(query, location)
            fallback_results = self._search_with_duckduckgo(query, location)
            return fallback_results if fallback_results else self._mock_results(query, location)

    def _get_google_place_details(self, place_id: str) -> Dict:
        """
        Fetch detailed fields for a Google Place.

        Args:
            place_id: Google Places place_id

        Returns:
            Dict containing details fields
        """
        try:
            details_url = "https://maps.googleapis.com/maps/api/place/details/json"
            response = requests.get(
                details_url,
                params={
                    "place_id": place_id,
                    "fields": "name,formatted_address,formatted_phone_number,international_phone_number,website,rating",
                    "key": self.google_places_key,
                },
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

            if data.get("status") != "OK":
                logger.debug("Google Place Details status=%s for place_id=%s", data.get("status"), place_id)
                return {}

            return data.get("result", {})

        except Exception:
            logger.debug("Google Place Details failed for place_id=%s", place_id)
            return {}
    
    def _search_with_tavily(self, query: str, location: str) -> List[Dict]:
        """
        Real search using Tavily API
        
        Args:
            query: Search query
            location: Location context
            
        Returns:
            List of real search results from web
        """
        try:
            logger.info("Executing Tavily API search: query=%s location=%s", query, location)
            
            payload = {
                "api_key": self.tavily_key,
                "query": f"{query} in {location}",
                "max_results": 5,
                "include_answer": True,
                "search_depth": "basic"
            }
            
            response = requests.post(self.tavily_url, json=payload, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            # Parse Tavily results
            for result in data.get("results", []):
                phone = self._extract_phone_number(result.get("url", ""), result.get("content", ""))
                results.append({
                    "name": result.get("title", "Unknown"),
                    "location": location,
                    "type": query,
                    "rating": 4.0 + (hash(result.get("title", "")) % 10) / 10,  # Mock rating
                    "source": "tavily",
                    "url": result.get("url", "#"),
                    "snippet": result.get("content", "")[:100],
                    "phone": phone,
                })
            
            logger.info("Tavily returned %s result(s)", len(results))
            return results
            
        except Exception as e:
            logger.exception("Tavily search failed, falling back to mock results")
            return self._mock_results(query, location)

    def _search_with_duckduckgo(self, query: str, location: str) -> List[Dict]:
        """
        Public web search fallback using DuckDuckGo HTML results.

        Args:
            query: Search query
            location: Location context

        Returns:
            List of search results from public web pages
        """
        try:
            search_query = f"{query} in {location}"
            logger.info("Executing DuckDuckGo fallback search: query=%s", search_query)

            response = requests.get(
                "https://html.duckduckgo.com/html/",
                params={"q": search_query},
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/124.0.0.0 Safari/537.36"
                    )
                },
                timeout=10,
            )
            response.raise_for_status()

            results: List[Dict] = []
            matches = re.finditer(
                r'<a[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
                response.text,
                re.DOTALL,
            )

            for match in matches:
                if len(results) >= 5:
                    break

                url = match.group(1)
                title_html = match.group(2)
                title = re.sub(r"<.*?>", "", title_html).strip()
                if not title:
                    continue

                phone = self._extract_phone_number(url)

                results.append({
                    "name": title,
                    "location": location,
                    "type": query,
                    "rating": 4.0,
                    "source": "duckduckgo_web",
                    "url": url,
                    "snippet": f"Public web result for '{query}' in {location}",
                    "phone": phone,
                })

            logger.info("DuckDuckGo fallback returned %s result(s)", len(results))
            return results

        except Exception:
            logger.exception("DuckDuckGo fallback search failed")
            return []
    
    def _mock_results(self, query: str, location: str) -> List[Dict]:
        """
        Mock results (for demo/testing without API)
        
        Args:
            query: Search query
            location: Location context
            
        Returns:
            List of sample results
        """
        mock_data = {
            "plant nurseries": [
                f"{query.title()} #1 - {location}",
                f"{query.title()} #2 - {location}",
            ],
            "pots manufacturers": [
                f"XYZ Pottery Workshop - {location}",
                f"ABC Clay Works - {location}",
            ],
            "pottery manufacturers": [
                f"DEF Ceramics - {location}",
                f"GHI Handmade Pots - {location}",
            ],
        }
        
        base_results = mock_data.get(query, [
            f"{query} Result 1 - {location}",
            f"{query} Result 2 - {location}",
        ])
        
        results = []
        for idx, name in enumerate(base_results, 1):
            results.append({
                "name": name,
                "location": location,
                "type": query,
                "rating": 3.5 + (idx * 0.3),
                "source": "mock_demo",
                "url": "#",
                "snippet": f"Sample result for '{query}' in {location}",
                "phone": None,
            })
        
        logger.info("Returning %s mock result(s)", len(results))
        return results
    
    def search_multiple_queries(self, queries: List[str], location: str) -> Dict:
        """
        Search using multiple queries and aggregate results
        
        Args:
            queries: List of search queries
            location: Location to search in
            
        Returns:
            Dict with aggregated results
        """
        logger.info("Running multiple searches: %s query(ies) for location=%s", len(queries), location)
        all_results = {}
        
        for query in queries:
            results = self.search_places(query, location)
            all_results[query] = results
        
        logger.info("Completed multi-query search")
        return all_results
    
    def search_along_route(self, queries: List[str], waypoints: List[Dict]) -> Dict:
        """
        Search for businesses along entire route at multiple waypoints
        
        Args:
            queries: List of search queries
            waypoints: List of waypoint coordinates
            
        Returns:
            Dict with results organized by waypoint and query
        """
        logger.info("Searching along route: %s queries at %s waypoints", len(queries), len(waypoints))
        route_results = {}
        
        for idx, waypoint in enumerate(waypoints, 1):
            waypoint_name = f"Waypoint {idx}"
            route_results[waypoint_name] = self.search_multiple_queries(queries, waypoint_name)
        
        logger.info("Route search completed")
        return route_results

    def _extract_phone_number(self, url: str, content: str = "") -> Optional[str]:
        """
        Try to extract a phone number from a result URL or snippet content.

        Args:
            url: Page URL to fetch
            content: Optional page snippet or raw content

        Returns:
            Phone number if one can be found, otherwise None
        """
        patterns = [
            r"tel:([+\d][\d\s().-]{7,})",
            r"(?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{2,5}\)?[\s.-]?)?\d{3,5}[\s.-]?\d{4}",
        ]

        search_text = content or ""

        if url and url != "#":
            try:
                response = requests.get(
                    url,
                    headers={
                        "User-Agent": (
                            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                            "AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/124.0.0.0 Safari/537.36"
                        )
                    },
                    timeout=10,
                )
                if response.ok:
                    search_text = f"{search_text}\n{response.text}"
            except Exception:
                logger.debug("Phone extraction fetch failed for url=%s", url)

        for pattern in patterns:
            match = re.search(pattern, search_text)
            if match:
                phone = match.group(1) if match.groups() else match.group(0)
                phone = re.sub(r"\s+", " ", phone).strip()
                phone = phone.rstrip(".>,)")
                if len(re.sub(r"\D", "", phone)) >= 8:
                    return phone

        return None

