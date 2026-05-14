"""
AI Service - Handles Ollama integration for intelligent query generation
"""

import requests
import json
from typing import List, Optional

class AIService:
    """
    Service for generating intelligent search queries using Ollama (local LLM)
    """
    
    def __init__(self, ollama_url: str = "http://localhost:11434"):
        """
        Initialize AIService with Ollama endpoint
        
        Args:
            ollama_url: URL where Ollama is running (default: localhost:11434)
        """
        self.ollama_url = ollama_url
        self.model = "mistral"  # Default model, can be changed
        
    def check_ollama_connection(self) -> bool:
        """
        Check if Ollama is running and accessible
        
        Returns:
            True if Ollama is accessible, False otherwise
        """
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def generate_search_queries(self, source: str, destination: str, 
                               user_query: str) -> List[str]:
        """
        Generate intelligent search queries for locations along the route
        
        Args:
            source: Source location name
            destination: Destination location name
            user_query: What user wants to find (e.g., "plant nurseries")
            
        Returns:
            List of search queries to use for finding businesses
        """
        try:
            prompt = f"""You are a helpful assistant that generates search queries for finding businesses along a route.

Source: {source}
Destination: {destination}
User is looking for: {user_query}

Generate exactly 3-5 relevant search queries that would help find {user_query} along the route from {source} to {destination}.

Format your response as a simple numbered list, nothing else.
Example:
1. {user_query} near {source}
2. {user_query} on highway between {source} and {destination}
3. wholesale {user_query} {destination} region
"""
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                text = result.get("response", "")
                
                # Parse queries from response
                queries = []
                for line in text.split("\n"):
                    line = line.strip()
                    if line and not line.startswith("#"):
                        # Remove numbering if present
                        if line[0].isdigit():
                            line = line.split(".", 1)[-1].strip()
                        if line:
                            queries.append(line)
                
                return queries if queries else [user_query]
            
            return [user_query]
            
        except Exception as e:
            print(f"Error generating queries with Ollama: {e}")
            # Fallback to simple query generation
            return self._fallback_queries(user_query, source, destination)
    
    def _fallback_queries(self, query: str, source: str, destination: str) -> List[str]:
        """
        Fallback query generation if Ollama is not available
        
        Args:
            query: User's search query
            source: Source location
            destination: Destination location
            
        Returns:
            List of simple search queries
        """
        return [
            query,
            f"{query} near {source}",
            f"{query} {destination}",
            f"best {query} {source} to {destination}"
        ]
