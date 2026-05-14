"""
Route Service - Handles OpenRouteService API calls for route and geocoding
"""

import requests
from typing import Dict, List, Tuple, Optional

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
                
                return {
                    "name": feature.get("properties", {}).get("name", location),
                    "latitude": coords[1],
                    "longitude": coords[0],
                    "full_name": feature.get("properties", {}).get("label", location)
                }
            return None
            
        except Exception as e:
            print(f"Error geocoding location {location}: {e}")
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
                [source_coords[1], source_coords[0]],
                [dest_coords[1], dest_coords[0]]
            ]
            
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
                
                return {
                    "distance": route.get("summary", {}).get("distance", 0),
                    "duration": route.get("summary", {}).get("duration", 0),
                    "geometry": route.get("geometry"),
                    "segments": route.get("segments", [])
                }
            return None
            
        except Exception as e:
            print(f"Error getting route: {e}")
            return None
    
    def extract_towns_from_route(self, route_geometry: Dict) -> List[Dict]:
        """
        Extract major towns/waypoints along the route (MVP version)
        Uses a simple approach - we'll enhance this later
        
        Args:
            route_geometry: Route geometry from get_route()
            
        Returns:
            List of town/waypoint dicts with coordinates
        """
        try:
            if not route_geometry:
                return []
            
            # Get coordinates from geometry
            coords = route_geometry.get("coordinates", [])
            
            if len(coords) < 3:
                return []
            
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
