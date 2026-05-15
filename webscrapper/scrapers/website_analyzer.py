"""
Website Analyzer
Analyzes school websites for quality indicators and digital presence
"""

import logging
import requests
from typing import Dict, Optional
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import ssl
import socket
from datetime import datetime

logger = logging.getLogger(__name__)


class WebsiteAnalyzer:
    """
    Analyzes school websites for digital quality indicators:
    - SSL/HTTPS presence
    - Mobile responsiveness
    - Website structure and age
    - Broken links
    - Contact information
    """
    
    def __init__(self, timeout: int = 10):
        """
        Initialize WebsiteAnalyzer
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        logger.info("WebsiteAnalyzer initialized with timeout=%ds", timeout)
    
    def analyze(self, url: Optional[str]) -> Dict:
        """
        Perform comprehensive analysis on a website
        
        Args:
            url: Website URL to analyze
            
        Returns:
            Dictionary with analysis results
        """
        analysis = {
            'has_website': False,
            'url': url,
            'is_accessible': False,
            'has_ssl': False,
            'is_mobile_friendly': False,
            'has_contact': False,
            'has_social': False,
            'html_age_indicator': 'unknown',
            'broken_links': 0,
            'status_code': None,
            'response_time': None,
            'issues': []
        }
        
        if not url:
            analysis['issues'].append('No website URL provided')
            logger.debug("No URL to analyze")
            return analysis
        
        analysis['has_website'] = True
        
        # Normalize URL
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        try:
            logger.debug("Analyzing website: %s", url)
            
            # Check SSL
            analysis['has_ssl'] = self._check_ssl(url)
            
            # Fetch and analyze HTML
            response = self._fetch_website(url)
            
            if response:
                analysis['is_accessible'] = True
                analysis['status_code'] = response.status_code
                analysis['response_time'] = response.elapsed.total_seconds()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Analyze HTML structure
                analysis['is_mobile_friendly'] = self._check_mobile_friendly(soup)
                analysis['has_contact'] = self._check_contact_info(soup)
                analysis['has_social'] = self._check_social_links(soup)
                analysis['html_age_indicator'] = self._estimate_html_age(soup)
                analysis['broken_links'] = self._count_broken_links(soup, url)
            else:
                analysis['issues'].append('Website is not accessible')
        
        except Exception as e:
            analysis['issues'].append(f'Analysis error: {str(e)}')
            logger.error("Error analyzing website %s: %s", url, str(e))
        
        logger.debug("Analysis complete for %s: %s", url, analysis)
        return analysis
    
    def _check_ssl(self, url: str) -> bool:
        """
        Check if website has valid SSL certificate
        
        Args:
            url: Website URL
            
        Returns:
            True if SSL is valid
        """
        try:
            parsed_url = urlparse(url)
            hostname = parsed_url.netloc
            
            context = ssl.create_default_context()
            with socket.create_connection((hostname, 443), timeout=self.timeout) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    has_ssl = cert is not None
                    logger.debug("SSL check for %s: %s", hostname, has_ssl)
                    return has_ssl
        except Exception as e:
            logger.debug("SSL check failed for %s: %s", url, str(e))
            return False
    
    def _fetch_website(self, url: str) -> Optional[requests.Response]:
        """
        Fetch website content
        
        Args:
            url: Website URL
            
        Returns:
            Response object or None if failed
        """
        try:
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            response.raise_for_status()
            logger.debug("Successfully fetched %s (status: %d)", url, response.status_code)
            return response
        except Exception as e:
            logger.debug("Failed to fetch %s: %s", url, str(e))
            return None
    
    def _check_mobile_friendly(self, soup: BeautifulSoup) -> bool:
        """
        Check if website has mobile viewport meta tag
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            True if mobile-friendly indicators found
        """
        try:
            # Check for viewport meta tag
            viewport = soup.find('meta', attrs={'name': 'viewport'})
            if not viewport:
                logger.debug("No viewport meta tag found")
                return False
            
            logger.debug("Viewport meta tag found")
            return True
        except Exception as e:
            logger.error("Error checking mobile-friendly: %s", str(e))
            return False
    
    def _check_contact_info(self, soup: BeautifulSoup) -> bool:
        """
        Check if website has contact information
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            True if contact info found
        """
        try:
            # Look for contact indicators
            text = soup.get_text().lower()
            contact_keywords = ['contact', 'email', 'phone', 'call us', 'reach us']
            
            has_contact = any(keyword in text for keyword in contact_keywords)
            logger.debug("Contact info check: %s", has_contact)
            return has_contact
        except Exception as e:
            logger.error("Error checking contact info: %s", str(e))
            return False
    
    def _check_social_links(self, soup: BeautifulSoup) -> bool:
        """
        Check if website has social media links
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            True if social links found
        """
        try:
            links = soup.find_all('a', href=True)
            social_domains = ['facebook.com', 'twitter.com', 'instagram.com', 'linkedin.com', 'youtube.com']
            
            has_social = any(
                any(domain in link.get('href', '').lower() for domain in social_domains)
                for link in links
            )
            logger.debug("Social links check: %s", has_social)
            return has_social
        except Exception as e:
            logger.error("Error checking social links: %s", str(e))
            return False
    
    def _estimate_html_age(self, soup: BeautifulSoup) -> str:
        """
        Estimate HTML structure age based on tags and structure
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            Age indicator: 'modern', 'older', or 'unknown'
        """
        try:
            # Check for modern HTML5 semantic tags
            modern_tags = soup.find_all(['header', 'nav', 'main', 'footer', 'article', 'section'])
            
            # Check for outdated layout approaches
            tables_for_layout = soup.find_all('table')
            deprecated_tags = soup.find_all(['font', 'center', 'blink'])
            
            if len(modern_tags) > 5 and len(deprecated_tags) == 0:
                age = 'modern'
            elif len(deprecated_tags) > 0 or (len(tables_for_layout) > 3 and len(modern_tags) == 0):
                age = 'older'
            else:
                age = 'mixed'
            
            logger.debug("HTML age estimate: %s (modern_tags=%d, deprecated=%d)", 
                        age, len(modern_tags), len(deprecated_tags))
            return age
        except Exception as e:
            logger.error("Error estimating HTML age: %s", str(e))
            return 'unknown'
    
    def _count_broken_links(self, soup: BeautifulSoup, base_url: str) -> int:
        """
        Check for broken internal links
        
        Args:
            soup: BeautifulSoup object
            base_url: Base URL for resolving relative links
            
        Returns:
            Count of broken links found
        """
        try:
            links = soup.find_all('a', href=True)
            broken_count = 0
            checked = 0
            
            for link in links[:10]:  # Check only first 10 links to save time
                href = link.get('href', '')
                
                # Skip non-HTTP links
                if href.startswith(('mailto:', 'tel:', '#', 'javascript:')):
                    continue
                
                # Resolve relative URLs
                full_url = urljoin(base_url, href)
                
                # Skip external links
                if not full_url.startswith(base_url.split('/')[0:3].__str__()):
                    continue
                
                checked += 1
                
                try:
                    response = self.session.head(full_url, timeout=3)
                    if response.status_code >= 400:
                        broken_count += 1
                        logger.debug("Broken link found: %s (status: %d)", full_url, response.status_code)
                except:
                    broken_count += 1
            
            logger.debug("Link check complete: %d broken out of %d checked", broken_count, checked)
            return broken_count
        except Exception as e:
            logger.error("Error counting broken links: %s", str(e))
            return 0
    
    def close(self):
        """Clean up resources"""
        self.session.close()
        logger.info("WebsiteAnalyzer closed")
