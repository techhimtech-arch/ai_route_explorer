"""
AI Service - Handles Ollama integration for intelligent query generation
"""

import logging
import requests
from typing import List, Optional


logger = logging.getLogger(__name__)

class AIService:
    """
    Service for generating intelligent search queries using Ollama (local LLM)
    """
    
    def __init__(self, ollama_url: str = "http://localhost:11434", model: str = "mistral"):
        """
        Initialize AIService with Ollama endpoint
        
        Args:
            ollama_url: URL where Ollama is running (default: localhost:11434)
        """
        self.ollama_url = ollama_url
        self.model = model
        logger.info("AIService initialized with ollama_url=%s model=%s", ollama_url, model)
        
    def check_ollama_connection(self) -> bool:
        """
        Check if Ollama is running and accessible
        
        Returns:
            True if Ollama is accessible, False otherwise
        """
        try:
            logger.info("Checking Ollama connection")
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            connected = response.status_code == 200
            logger.info("Ollama connection status=%s", connected)
            return connected
        except Exception:
            logger.exception("Ollama connection check failed")
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
            logger.info(
                "Generating search queries for source=%s destination=%s user_query=%s",
                source,
                destination,
                user_query,
            )
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
                logger.debug("Raw Ollama response: %s", text)
                
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
                
                logger.info("Parsed %s query(ies) from Ollama", len(queries))
                return queries if queries else [user_query]
            
            logger.warning("Ollama returned status code %s", response.status_code)
            return [user_query]
            
        except Exception as e:
            logger.exception("Error generating queries with Ollama")
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
        logger.info("Using fallback query generation")
        return [
            query,
            f"{query} near {source}",
            f"{query} {destination}",
            f"best {query} {source} to {destination}"
        ]
