"""
Route Service - Handles OpenRouteService API calls for route and geocoding
"""

import logging
import requests
from typing import Dict, List, Tuple, Optional


logger = logging.getLogger(__name__)

class RouteService:
    """
    Service for fetching routes and geocoding locations using OpenRouteService API
    """
    
    def __init__(self, api_key: str):
        """
        Initialize RouteService with API key
        
        Args:
            api_key: OpenRouteService API key
        """
        self.api_key = api_key
        self.base_url = "https://api.openrouteservice.org"
        
    def geocode_location(self, location: str) -> Optional[Dict]:
        """
        Convert location name to coordinates (lat, lon)
        
        Args:
            location: Location name (e.g., "Shimla")
            
        Returns:
            Dict with coordinates and location info, or None if not found
        """
        try:
            logger.info("Geocoding location: %s", location)
            url = f"{self.base_url}/geocode/search"
            params = {
                "api_key": self.api_key,
                "text": location
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract first result if available
            if data.get("features") and len(data["features"]) > 0:
                feature = data["features"][0]
                coords = feature["geometry"]["coordinates"]
                logger.info("Geocoding successful for %s -> lon=%s lat=%s", location, coords[0], coords[1])
                
                return {
                    "name": feature.get("properties", {}).get("name", location),
                    "latitude": coords[1],
                    "longitude": coords[0],
                    "full_name": feature.get("properties", {}).get("label", location)
                }
            logger.warning("No geocoding results found for %s", location)
            return None
            
        except Exception as e:
            logger.exception("Error geocoding location %s", location)
            return None
    
    def get_route(self, source_coords: Tuple[float, float], 
                  dest_coords: Tuple[float, float]) -> Optional[Dict]:
        """
        Get route between two coordinates
        
        Args:
            source_coords: Tuple of (longitude, latitude) for source
            dest_coords: Tuple of (longitude, latitude) for destination
            
        Returns:
            Dict with route details, or None if request fails
        """
        try:
            url = f"{self.base_url}/v2/directions/driving-car"
            
            # OpenRouteService expects [lon, lat] format
            coordinates = [
                [source_coords[0], source_coords[1]],
                [dest_coords[0], dest_coords[1]]
            ]
            logger.info("Requesting route with coordinates=%s", coordinates)
            
            params = {
                "api_key": self.api_key,
            }
            
            json_data = {
                "coordinates": coordinates,
                "extra_info": ["way_category", "surface"]
            }
            
            response = requests.post(url, params=params, json=json_data, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("routes") and len(data["routes"]) > 0:
                route = data["routes"][0]
                logger.info(
                    "Route received: distance=%s duration=%s",
                    route.get("summary", {}).get("distance", 0),
                    route.get("summary", {}).get("duration", 0),
                )
                
                return {
                    "distance": route.get("summary", {}).get("distance", 0),
                    "duration": route.get("summary", {}).get("duration", 0),
                    "geometry": route.get("geometry"),
                    "segments": route.get("segments", [])
                }
            logger.warning("Route API returned no routes")
            return None
            
        except Exception as e:
            logger.exception("Error getting route")
            return None
    
    def extract_towns_from_route(self, route_geometry: Dict) -> List[Dict]:
        """
        Extract major towns/waypoints along the route (MVP version)
        Uses a simple approach - we'll enhance this later
        
        Args:
            route_geometry: Route geometry from get_route()
            
        Returns:
            logger.info("Extracting waypoints from route geometry")
            # MVP approach: return sample waypoints for now
        """
        try:
            if not route_geometry:
                return []
            
            # Get coordinates from geometry
            coords = route_geometry.get("coordinates", [])
            
            logger.info("Extracted %s waypoint(s)", len(waypoints))
            if len(coords) < 3:
                return []
            logger.exception("Error extracting towns from route")
            # Simple MVP: extract waypoints at regular intervals
            # Format: [lon, lat]
            num_points = len(coords)
            interval = max(num_points // 5, 1)  # Get ~5 waypoints
            
            waypoints = []
            for i in range(0, num_points, interval):
                if i < num_points:
                    lon, lat = coords[i]
                    waypoints.append({
                        "latitude": lat,
                        "longitude": lon,
                        "index": i,
                        "type": "waypoint"
                    })
            
            return waypoints
            
        except Exception as e:
            print(f"Error extracting towns: {e}")
            return []
