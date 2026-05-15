"""
Export Service
Handles exporting scan results to CSV and other formats
"""

import logging
import pandas as pd
from typing import List, Dict, Optional
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


class ExportService:
    """
    Exports scan results to various formats (CSV, JSON, etc.)
    Creates business-ready reports with leads
    """
    
    def __init__(self, export_dir: str = 'exports'):
        """
        Initialize ExportService
        
        Args:
            export_dir: Directory to save exports
        """
        self.export_dir = Path(export_dir)
        self.export_dir.mkdir(parents=True, exist_ok=True)
        logger.info("ExportService initialized with export_dir=%s", export_dir)
    
    def export_to_csv(self, scores: List[Dict], filename: Optional[str] = None) -> str:
        """
        Export scores to CSV file
        
        Args:
            scores: List of score dictionaries
            filename: Custom filename (auto-generated if None)
            
        Returns:
            Path to exported file
        """
        try:
            # Prepare data for CSV
            csv_data = self._prepare_csv_data(scores)
            
            # Generate filename
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"school_scan_{timestamp}.csv"
            
            filepath = self.export_dir / filename
            
            # Write CSV
            csv_data.to_csv(filepath, index=False, encoding='utf-8')
            
            logger.info("Exported %d records to %s", len(scores), filepath)
            return str(filepath)
        
        except Exception as e:
            logger.error("Error exporting to CSV: %s", str(e))
            raise
    
    def export_to_leads_csv(self, scores: List[Dict], filename: Optional[str] = None) -> str:
        """
        Export high-priority leads (no website or broken website)
        
        Args:
            scores: List of score dictionaries
            filename: Custom filename (auto-generated if None)
            
        Returns:
            Path to exported file
        """
        try:
            # Filter for leads (gap type indicates sales opportunity)
            leads = [
                score for score in scores
                if score.get('gap_type') in [
                    'No Digital Presence',
                    'Broken Website',
                    'Outdated Design',
                    'Security Gap'
                ]
            ]
            
            logger.info("Found %d leads from %d schools", len(leads), len(scores))
            
            # Prepare leads data
            leads_data = self._prepare_leads_csv_data(leads)
            
            # Generate filename
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"leads_hotlist_{timestamp}.csv"
            
            filepath = self.export_dir / filename
            
            # Write CSV
            leads_data.to_csv(filepath, index=False, encoding='utf-8')
            
            logger.info("Exported %d leads to %s", len(leads), filepath)
            return str(filepath)
        
        except Exception as e:
            logger.error("Error exporting leads: %s", str(e))
            raise
    
    def export_summary_report(self, scores: List[Dict], city: str, state: str, 
                            filename: Optional[str] = None) -> str:
        """
        Export summary report with statistics
        
        Args:
            scores: List of score dictionaries
            city: City searched
            state: State searched
            filename: Custom filename (auto-generated if None)
            
        Returns:
            Path to exported file
        """
        try:
            # Generate filename
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"summary_{city}_{state}_{timestamp}.txt"
            
            filepath = self.export_dir / filename
            
            # Generate report
            report = self._generate_summary_report(scores, city, state)
            
            # Write report
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report)
            
            logger.info("Exported summary report to %s", filepath)
            return str(filepath)
        
        except Exception as e:
            logger.error("Error exporting summary report: %s", str(e))
            raise
    
    def _prepare_csv_data(self, scores: List[Dict]) -> pd.DataFrame:
        """
        Prepare score data for CSV export
        
        Args:
            scores: List of score dictionaries
            
        Returns:
            DataFrame formatted for CSV
        """
        records = []
        
        for score in scores:
            breakdown = score.get('breakdown', {})
            
            record = {
                'School Name': score.get('school_name', ''),
                'Website URL': score.get('website_url', 'No Website'),
                'Status': score.get('status', ''),
                'Gap Type': score.get('gap_type', ''),
                'Digital Score': score.get('total_score', 0),
                'Grade': score.get('grade', 'F'),
                'Has Website': 'Yes' if score.get('website_url') else 'No',
                'Has SSL': 'Yes' if breakdown.get('ssl_security', 0) > 0 else 'No',
                'Mobile Friendly': 'Yes' if breakdown.get('mobile_friendly', 0) > 0 else 'No',
                'Has Contact': 'Yes' if breakdown.get('contact_info', 0) > 0 else 'No',
                'Social Links': 'Yes' if breakdown.get('social_presence', 0) > 0 else 'No',
                'HTML Quality': 'Modern' if breakdown.get('html_quality', 0) > 10 else 'Older',
                'Key Issues': ' | '.join(score.get('key_issues', [])),
            }
            records.append(record)
        
        df = pd.DataFrame(records)
        logger.debug("Prepared CSV data: %d records", len(records))
        return df
    
    def _prepare_leads_csv_data(self, leads: List[Dict]) -> pd.DataFrame:
        """
        Prepare lead data for leads CSV (sales-focused)
        
        Args:
            leads: List of lead dictionaries
            
        Returns:
            DataFrame formatted for sales
        """
        records = []
        
        for lead in leads:
            record = {
                'School Name': lead.get('school_name', ''),
                'Current Website': lead.get('website_url', 'No Website'),
                'Opportunity Type': lead.get('gap_type', ''),
                'Priority': self._calculate_priority(lead),
                'Current Score': lead.get('total_score', 0),
                'Key Issues': ' | '.join(lead.get('key_issues', [])),
                'Sales Pitch': self._generate_sales_pitch(lead),
                'Recommended Services': self._get_recommended_services(lead),
            }
            records.append(record)
        
        df = pd.DataFrame(records)
        logger.debug("Prepared leads CSV data: %d records", len(records))
        return df
    
    def _calculate_priority(self, score: Dict) -> str:
        """
        Calculate lead priority for sales
        
        Args:
            score: Score dictionary
            
        Returns:
            Priority level (HOT, WARM, COOL)
        """
        gap_type = score.get('gap_type', '')
        total_score = score.get('total_score', 0)
        
        if gap_type == 'No Digital Presence':
            return 'HOT 🔥'
        elif gap_type == 'Broken Website':
            return 'HOT 🔥'
        elif gap_type == 'Outdated Design' and total_score < 50:
            return 'WARM 🔥'
        else:
            return 'COOL'
    
    def _generate_sales_pitch(self, score: Dict) -> str:
        """
        Generate sales pitch based on gap
        
        Args:
            score: Score dictionary
            
        Returns:
            Short sales pitch
        """
        gap_type = score.get('gap_type', '')
        
        pitches = {
            'No Digital Presence': 'Schools without websites lose students and funding',
            'Broken Website': 'Non-functional website damages school reputation',
            'Outdated Design': 'Outdated design drives families to competitor schools',
            'Security Gap': 'Missing SSL puts student data at risk',
            'Mobile Gap': 'Mobile-unfriendly site limits access from mobile users',
        }
        
        return pitches.get(gap_type, 'Digital presence improvement opportunity')
    
    def _get_recommended_services(self, score: Dict) -> str:
        """
        Suggest services based on gaps
        
        Args:
            score: Score dictionary
            
        Returns:
            Recommended services
        """
        recommendations = []
        gap_type = score.get('gap_type', '')
        
        if gap_type == 'No Digital Presence':
            recommendations = ['Website Design', 'SEO', 'Setup']
        elif gap_type == 'Broken Website':
            recommendations = ['Website Repair', 'Hosting']
        elif gap_type == 'Outdated Design':
            recommendations = ['Website Redesign', 'Mobile Optimization']
        elif gap_type == 'Security Gap':
            recommendations = ['SSL Certificate', 'Security Audit']
        elif gap_type == 'Mobile Gap':
            recommendations = ['Mobile Optimization', 'Responsive Design']
        
        return ', '.join(recommendations)
    
    def _generate_summary_report(self, scores: List[Dict], city: str, state: str) -> str:
        """
        Generate text summary report
        
        Args:
            scores: List of score dictionaries
            city: City name
            state: State name
            
        Returns:
            Report text
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Calculate statistics
        total_schools = len(scores)
        avg_score = sum(s.get('total_score', 0) for s in scores) / max(total_schools, 1)
        
        gap_counts = {}
        for score in scores:
            gap = score.get('gap_type', 'Unknown')
            gap_counts[gap] = gap_counts.get(gap, 0) + 1
        
        grade_counts = {}
        for score in scores:
            grade = score.get('grade', 'F')
            grade_counts[grade] = grade_counts.get(grade, 0) + 1
        
        leads_count = sum(1 for s in scores if s.get('gap_type') in [
            'No Digital Presence', 'Broken Website', 'Outdated Design', 'Security Gap'
        ])
        
        report = f"""
╔═══════════════════════════════════════════════════════════════════╗
║           SCHOOL DIGITAL GAP ANALYSIS REPORT                      ║
╚═══════════════════════════════════════════════════════════════════╝

Report Generated: {timestamp}
Location: {city}, {state}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 OVERVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Schools Analyzed: {total_schools}
Average Digital Score: {avg_score:.1f}/100
Sales Leads Identified: {leads_count}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 DIGITAL SCORE DISTRIBUTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        for grade in ['A', 'B', 'C', 'D', 'F']:
            count = grade_counts.get(grade, 0)
            percentage = (count / max(total_schools, 1)) * 100
            bar = '█' * int(percentage / 5)
            report += f"Grade {grade}: {count:3d} schools ({percentage:5.1f}%) {bar}\n"
        
        report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 DIGITAL GAPS IDENTIFIED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        for gap_type, count in sorted(gap_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / max(total_schools, 1)) * 100
            report += f"  • {gap_type}: {count} schools ({percentage:.1f}%)\n"
        
        report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💼 BUSINESS OPPORTUNITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HIGH-PRIORITY LEADS: {leads_count} schools
These schools represent immediate opportunities for:
  ✓ Website development/redesign services
  ✓ Digital strategy consulting
  ✓ SEO and online visibility services
  ✓ Mobile optimization services
  ✓ Security and compliance services

ESTIMATED MARKET VALUE:
  • {leads_count} schools × $3,000-$15,000 per project
  • Potential revenue: ${leads_count * 3000:,} - ${leads_count * 15000:,}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 DETAILED RESULTS
See attached CSV file for complete school list and contact details.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        logger.debug("Summary report generated")
        return report
