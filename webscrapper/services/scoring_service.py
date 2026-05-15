"""
Scoring Service
Generates digital quality scores for schools based on website analysis
"""

import logging
from typing import Dict, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ScoreBreakdown:
    """Score breakdown with component weights"""
    website_presence: float = 20.0  # Has website
    ssl_security: float = 15.0      # Has SSL
    mobile_friendly: float = 20.0   # Mobile responsive
    contact_info: float = 15.0      # Contact form/info
    social_presence: float = 10.0   # Social links
    html_quality: float = 15.0      # Modern HTML structure
    link_quality: float = 5.0       # No broken links


class ScoringService:
    """
    Calculates digital quality scores for schools
    Score range: 0-100
    
    Scoring formula:
    - No website: 0-15 points (critical gap)
    - Basic website without SSL: 15-35 points
    - Website with SSL but not mobile: 35-60 points
    - Website with SSL + mobile + contact: 60-85 points
    - Modern website with all features: 85-100 points
    """
    
    def __init__(self, breakdown: ScoreBreakdown = None):
        """
        Initialize ScoringService
        
        Args:
            breakdown: Custom score breakdown (default uses standard)
        """
        self.breakdown = breakdown or ScoreBreakdown()
        self.total_weight = sum([
            self.breakdown.website_presence,
            self.breakdown.ssl_security,
            self.breakdown.mobile_friendly,
            self.breakdown.contact_info,
            self.breakdown.social_presence,
            self.breakdown.html_quality,
            self.breakdown.link_quality
        ])
        logger.info("ScoringService initialized with total_weight=%.1f", self.total_weight)
    
    def calculate_score(self, school: Dict, analysis: Dict) -> Dict:
        """
        Calculate digital quality score for a school
        
        Args:
            school: School dictionary with basic info
            analysis: Website analysis results
            
        Returns:
            Dictionary with score and breakdown
        """
        score_result = {
            'school_name': school.get('name', 'Unknown'),
            'website_url': analysis.get('url'),
            'total_score': 0,
            'grade': 'F',
            'status': 'No Digital Presence',
            'gap_type': 'Unknown',
            'breakdown': {},
            'key_issues': [],
            'recommendations': []
        }
        
        # Calculate component scores
        components = self._calculate_components(analysis)
        
        # Calculate weighted total
        total_score = sum(components.values())
        
        # Normalize to 0-100 scale
        normalized_score = (total_score / self.total_weight) * 100
        score_result['total_score'] = round(normalized_score, 1)
        
        # Generate grade and status
        score_result['grade'] = self._get_grade(score_result['total_score'])
        score_result['status'] = self._get_status(analysis)
        score_result['gap_type'] = self._get_gap_type(analysis)
        
        # Add breakdown
        score_result['breakdown'] = components
        
        # Generate issues and recommendations
        score_result['key_issues'] = self._identify_issues(analysis)
        score_result['recommendations'] = self._generate_recommendations(analysis)
        
        logger.info(
            "Score calculated for %s: %.1f (%s) - %s",
            school.get('name', 'Unknown'),
            score_result['total_score'],
            score_result['grade'],
            score_result['gap_type']
        )
        
        return score_result
    
    def _calculate_components(self, analysis: Dict) -> Dict[str, float]:
        """
        Calculate individual component scores
        
        Args:
            analysis: Website analysis results
            
        Returns:
            Dictionary of component scores
        """
        components = {}
        
        # Website presence (0 or 20 points)
        components['website_presence'] = (
            self.breakdown.website_presence if analysis.get('has_website') else 0
        )
        
        # SSL security (0 or 15 points)
        components['ssl_security'] = (
            self.breakdown.ssl_security if analysis.get('has_ssl') else 0
        )
        
        # Mobile friendly (0 or 20 points)
        components['mobile_friendly'] = (
            self.breakdown.mobile_friendly if analysis.get('is_mobile_friendly') else 0
        )
        
        # Contact info (0 or 15 points)
        components['contact_info'] = (
            self.breakdown.contact_info if analysis.get('has_contact') else 0
        )
        
        # Social presence (0 or 10 points)
        components['social_presence'] = (
            self.breakdown.social_presence if analysis.get('has_social') else 0
        )
        
        # HTML quality (0-15 points based on age)
        html_age = analysis.get('html_age_indicator', 'unknown')
        if html_age == 'modern':
            components['html_quality'] = self.breakdown.html_quality
        elif html_age == 'older':
            components['html_quality'] = self.breakdown.html_quality * 0.4
        else:
            components['html_quality'] = self.breakdown.html_quality * 0.6
        
        # Link quality (0-5 points based on broken links)
        broken_links = analysis.get('broken_links', 0)
        if broken_links == 0:
            components['link_quality'] = self.breakdown.link_quality
        elif broken_links == 1:
            components['link_quality'] = self.breakdown.link_quality * 0.7
        else:
            components['link_quality'] = max(0, self.breakdown.link_quality * (1 - broken_links * 0.2))
        
        logger.debug("Component scores calculated: %s", components)
        return components
    
    def _get_grade(self, score: float) -> str:
        """
        Convert numeric score to letter grade
        
        Args:
            score: Numeric score (0-100)
            
        Returns:
            Letter grade A-F
        """
        if score >= 85:
            return 'A'
        elif score >= 75:
            return 'B'
        elif score >= 65:
            return 'C'
        elif score >= 50:
            return 'D'
        else:
            return 'F'
    
    def _get_status(self, analysis: Dict) -> str:
        """
        Get website status description
        
        Args:
            analysis: Website analysis results
            
        Returns:
            Status description
        """
        if not analysis.get('has_website'):
            return 'No Website'
        elif not analysis.get('is_accessible'):
            return 'Website Not Accessible'
        elif not analysis.get('has_ssl'):
            return 'No SSL Certificate'
        elif not analysis.get('is_mobile_friendly'):
            return 'Not Mobile Friendly'
        elif analysis.get('html_age_indicator') == 'older':
            return 'Outdated Website'
        else:
            return 'Modern Website'
    
    def _get_gap_type(self, analysis: Dict) -> str:
        """
        Identify the type of digital gap
        
        Args:
            analysis: Website analysis results
            
        Returns:
            Type of digital gap
        """
        if not analysis.get('has_website'):
            return 'No Digital Presence'
        elif not analysis.get('is_accessible'):
            return 'Broken Website'
        elif not analysis.get('has_ssl'):
            return 'Security Gap'
        elif not analysis.get('is_mobile_friendly'):
            return 'Mobile Gap'
        elif analysis.get('html_age_indicator') == 'older':
            return 'Outdated Design'
        else:
            return 'Opportunity for Enhancement'
    
    def _identify_issues(self, analysis: Dict) -> List[str]:
        """
        Identify key digital issues
        
        Args:
            analysis: Website analysis results
            
        Returns:
            List of identified issues
        """
        issues = []
        
        if not analysis.get('has_website'):
            issues.append('❌ No website - Lost online visibility')
        
        if analysis.get('has_website') and not analysis.get('is_accessible'):
            issues.append('❌ Website is broken/unreachable')
        
        if analysis.get('has_website') and not analysis.get('has_ssl'):
            issues.append('⚠️  No SSL - Security risk, browsers may warn visitors')
        
        if analysis.get('has_website') and not analysis.get('is_mobile_friendly'):
            issues.append('📱 Not mobile-friendly - Poor experience for 60%+ mobile users')
        
        if analysis.get('html_age_indicator') == 'older':
            issues.append('📅 Outdated design - Users perceive as unprofessional')
        
        if analysis.get('has_website') and not analysis.get('has_contact'):
            issues.append('📞 Missing contact information')
        
        if analysis.get('broken_links', 0) > 0:
            issues.append(f'🔗 {analysis["broken_links"]} broken links - Poor user experience')
        
        return issues
    
    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """
        Generate actionable recommendations
        
        Args:
            analysis: Website analysis results
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        if not analysis.get('has_website'):
            recommendations.append('🎯 **Priority #1**: Build a professional website (high ROI)')
            recommendations.append('💼 Include school info, contact, programs, and news section')
            recommendations.append('📱 Use responsive design (mobile-first)')
        
        if analysis.get('has_website') and not analysis.get('has_ssl'):
            recommendations.append('🔒 Install SSL certificate immediately (usually free)')
        
        if analysis.get('has_website') and not analysis.get('is_mobile_friendly'):
            recommendations.append('📱 Redesign for mobile responsiveness')
        
        if analysis.get('html_age_indicator') == 'older':
            recommendations.append('🔄 Modernize website design and technology stack')
        
        if analysis.get('has_website') and not analysis.get('has_social'):
            recommendations.append('📢 Add social media links (Facebook, Instagram, etc.)')
        
        if not analysis.get('has_contact'):
            recommendations.append('📧 Add clear contact information and contact form')
        
        return recommendations
    
    def batch_score_schools(self, schools: List[Dict], analyses: List[Dict]) -> List[Dict]:
        """
        Score multiple schools at once
        
        Args:
            schools: List of school dictionaries
            analyses: List of website analysis results
            
        Returns:
            List of score results
        """
        results = []
        
        for school, analysis in zip(schools, analyses):
            score = self.calculate_score(school, analysis)
            results.append(score)
        
        logger.info("Batch scoring complete: %d schools scored", len(results))
        return results
