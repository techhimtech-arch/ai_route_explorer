"""
School Digital Gap Scanner
AI-powered lead generation tool for website development services
Identifies schools with poor/no digital presence and generates business leads
"""

import logging
import streamlit as st
import os
from dotenv import load_dotenv
from datetime import datetime

# Import services and utilities
from scrapers import SchoolScraper, WebsiteAnalyzer
from services.scoring_service import ScoringService
from services.export_service import ExportService
from utils.logging_config import setup_logging
from utils import helpers

# ==================== Configuration ====================
load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
setup_logging(LOG_LEVEL)
logger = logging.getLogger(__name__)

logger.info("School Digital Gap Scanner starting")

# ==================== Page Configuration ====================
st.set_page_config(
    page_title="School Digital Gap Scanner",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    .gap-type-hot {
        background-color: #ffe0e0;
        padding: 10px;
        border-left: 4px solid #ff4444;
    }
    .gap-type-warm {
        background-color: #fff5e0;
        padding: 10px;
        border-left: 4px solid #ffaa00;
    }
    .gap-type-cool {
        background-color: #e0f2ff;
        padding: 10px;
        border-left: 4px solid #0088ff;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== Session State ====================
if 'scan_complete' not in st.session_state:
    st.session_state.scan_complete = False
    st.session_state.results = None
    st.session_state.schools = None

# ==================== Sidebar ====================
with st.sidebar:
    st.title("🎓 Scanner Configuration")
    
    col1, col2 = st.columns(2)
    with col1:
        city = st.text_input("City", placeholder="e.g., New York")
    with col2:
        state = st.text_input("State", placeholder="e.g., NY")
    
    num_schools = st.slider(
        "Schools to scan",
        min_value=5,
        max_value=100,
        value=20,
        step=5
    )
    
    st.divider()
    st.subheader("Scan Settings")
    
    timeout = st.slider(
        "Website timeout (seconds)",
        min_value=5,
        max_value=30,
        value=10
    )
    
    rate_limit = st.slider(
        "Rate limit delay (seconds)",
        min_value=0.5,
        max_value=3.0,
        value=1.0,
        step=0.5
    )
    
    check_ssl = st.checkbox("Check SSL", value=True)
    check_mobile = st.checkbox("Check Mobile Friendly", value=True)
    check_links = st.checkbox("Check Broken Links", value=False)
    
    st.divider()
    
    # Start scanning button
    if st.button("🔍 Start Scanning", use_container_width=True, type="primary"):
        if not city or not state:
            st.error("❌ Please enter both city and state")
        else:
            st.session_state.scan_complete = False
            st.session_state.results = None
            st.session_state.schools = None

# ==================== Main Content ====================
st.title("🎓 School Digital Gap Scanner")
st.markdown("""
    **Find schools with poor digital presence and generate business leads**
    
    This tool identifies schools that either:
    - ❌ Don't have a website
    - 🔗 Have broken or inaccessible websites
    - 🔒 Lack security (no SSL)
    - 📱 Are not mobile-friendly
    - 📅 Have outdated designs
    
    **Perfect for**: Web development agencies, SEO services, and digital marketing firms
""")

# ==================== Execute Scan ====================
if st.button("🔍 Start Scanning", use_container_width=True, type="primary") or (
    'city' in locals() and 'state' in locals() and city and state and not st.session_state.scan_complete
):
    if city and state:
        with st.spinner(f"🔎 Scanning schools in {city}, {state}..."):
            try:
                # Initialize services
                scraper = SchoolScraper(rate_limit_delay=rate_limit)
                analyzer = WebsiteAnalyzer(timeout=timeout)
                scorer = ScoringService()
                
                logger.info("Scan started for %s, %s", city, state)
                
                # Search for schools
                st.info("📍 Discovering schools...")
                schools = scraper.search_schools_by_city_state(city, state, num_schools)
                st.session_state.schools = schools
                
                if not schools:
                    st.warning("⚠️  No schools found for this location")
                    logger.warning("No schools found for %s, %s", city, state)
                else:
                    st.success(f"Found {len(schools)} schools")
                    
                    # Analyze websites
                    st.info("🌐 Analyzing websites...")
                    progress_bar = st.progress(0)
                    
                    analyses = []
                    for idx, school in enumerate(schools):
                        url = school.get('website')
                        analysis = analyzer.analyze(url)
                        analyses.append(analysis)
                        
                        progress = (idx + 1) / len(schools)
                        progress_bar.progress(progress)
                    
                    st.success("✅ Website analysis complete")
                    
                    # Score schools
                    st.info("📊 Calculating digital quality scores...")
                    scores = scorer.batch_score_schools(schools, analyses)
                    st.session_state.results = scores
                    st.session_state.scan_complete = True
                    st.success("✅ Scoring complete")
                    
                    logger.info("Scan completed: %d schools analyzed", len(schools))
                
                # Clean up
                scraper.close()
                analyzer.close()
            
            except Exception as e:
                st.error(f"❌ Error during scan: {str(e)}")
                logger.exception("Error during scan")

# ==================== Display Results ====================
if st.session_state.scan_complete and st.session_state.results:
    results = st.session_state.results
    schools = st.session_state.schools
    
    st.divider()
    st.header("📊 Scan Results")
    
    # Summary Statistics
    col1, col2, col3, col4 = st.columns(4)
    
    total_schools = len(results)
    avg_score = sum(r['total_score'] for r in results) / max(total_schools, 1)
    
    # Count gap types
    no_website = sum(1 for r in results if r['gap_type'] == 'No Digital Presence')
    broken = sum(1 for r in results if r['gap_type'] == 'Broken Website')
    outdated = sum(1 for r in results if r['gap_type'] == 'Outdated Design')
    leads = no_website + broken + outdated
    
    with col1:
        st.metric("Total Schools", total_schools, "analyzed")
    
    with col2:
        st.metric("Avg Score", f"{avg_score:.1f}/100", "digital quality")
    
    with col3:
        st.metric("🔴 No Website", no_website, "critical gap")
    
    with col4:
        st.metric("💼 Sales Leads", leads, f"{(leads/total_schools*100):.0f}%")
    
    st.divider()
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📋 All Schools", "🔥 Hot Leads", "📊 Statistics", "💾 Export"]
    )
    
    # ==================== TAB 1: All Schools ====================
    with tab1:
        st.subheader("Complete School List")
        
        # Display as sortable dataframe
        display_data = []
        for score in results:
            display_data.append({
                'School': score['school_name'],
                'Website': score['website_url'] or 'No Website',
                'Status': score['status'],
                'Score': score['total_score'],
                'Grade': score['grade'],
                'Gap Type': score['gap_type'],
            })
        
        st.dataframe(
            display_data,
            use_container_width=True,
            column_config={
                "Score": st.column_config.NumberColumn(format="%.1f"),
            }
        )
    
    # ==================== TAB 2: Hot Leads ====================
    with tab2:
        st.subheader("🔥 High-Priority Sales Leads")
        
        leads_list = [r for r in results if r['gap_type'] in [
            'No Digital Presence', 'Broken Website', 'Outdated Design'
        ]]
        
        if not leads_list:
            st.info("No high-priority leads found in this scan")
        else:
            st.success(f"Found {len(leads_list)} promising sales opportunities")
            
            for lead in sorted(leads_list, key=lambda x: x['total_score']):
                with st.expander(
                    f"{helpers.get_gap_type_icon(lead['gap_type'])} {lead['school_name']} - Score: {lead['total_score']:.0f}",
                    expanded=False
                ):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Website:** {lead['website_url'] or 'No Website'}")
                        st.write(f"**Grade:** {lead['grade']}")
                        st.write(f"**Gap Type:** {lead['gap_type']}")
                    
                    with col2:
                        st.write(f"**Status:** {lead['status']}")
                        st.write(f"**Digital Score:** {lead['total_score']:.1f}/100")
                    
                    st.write("**Key Issues:**")
                    for issue in lead['key_issues']:
                        st.write(f"  • {issue}")
                    
                    st.write("**Recommendations:**")
                    for rec in lead['recommendations']:
                        st.write(f"  • {rec}")
    
    # ==================== TAB 3: Statistics ====================
    with tab3:
        st.subheader("📊 Analysis Statistics")
        
        col1, col2 = st.columns(2)
        
        # Grade distribution
        with col1:
            st.write("**Score Distribution**")
            grade_counts = {}
            for r in results:
                grade = r['grade']
                grade_counts[grade] = grade_counts.get(grade, 0) + 1
            
            grade_data = [
                {"Grade": "A (85-100)", "Count": grade_counts.get('A', 0)},
                {"Grade": "B (75-84)", "Count": grade_counts.get('B', 0)},
                {"Grade": "C (65-74)", "Count": grade_counts.get('C', 0)},
                {"Grade": "D (50-64)", "Count": grade_counts.get('D', 0)},
                {"Grade": "F (<50)", "Count": grade_counts.get('F', 0)},
            ]
            
            st.bar_chart([d["Count"] for d in grade_data], use_container_width=True)
        
        # Gap types
        with col2:
            st.write("**Digital Gaps Identified**")
            gap_counts = {}
            for r in results:
                gap = r['gap_type']
                gap_counts[gap] = gap_counts.get(gap, 0) + 1
            
            gap_df = st.dataframe(
                [{"Gap Type": k, "Count": v} for k, v in gap_counts.items()],
                use_container_width=True,
                hide_index=True
            )
        
        st.divider()
        
        # Feature presence
        st.write("**Feature Presence Across All Schools**")
        col1, col2, col3, col4 = st.columns(4)
        
        has_website = sum(1 for r in results if r['website_url'])
        has_ssl = sum(1 for r in results if r['breakdown'].get('ssl_security', 0) > 0)
        is_mobile = sum(1 for r in results if r['breakdown'].get('mobile_friendly', 0) > 0)
        has_contact = sum(1 for r in results if r['breakdown'].get('contact_info', 0) > 0)
        
        with col1:
            pct = (has_website / max(total_schools, 1)) * 100
            st.metric("Has Website", f"{has_website}/{total_schools}", f"{pct:.0f}%")
        
        with col2:
            pct = (has_ssl / max(total_schools, 1)) * 100
            st.metric("Has SSL", f"{has_ssl}/{total_schools}", f"{pct:.0f}%")
        
        with col3:
            pct = (is_mobile / max(total_schools, 1)) * 100
            st.metric("Mobile Friendly", f"{is_mobile}/{total_schools}", f"{pct:.0f}%")
        
        with col4:
            pct = (has_contact / max(total_schools, 1)) * 100
            st.metric("Has Contact Info", f"{has_contact}/{total_schools}", f"{pct:.0f}%")
    
    # ==================== TAB 4: Export ====================
    with tab4:
        st.subheader("💾 Export Results")
        
        exporter = ExportService()
        
        col1, col2, col3 = st.columns(3)
        
        # Export all results
        with col1:
            if st.button("📥 Export All Schools (CSV)", use_container_width=True):
                try:
                    filepath = exporter.export_to_csv(results)
                    st.success(f"✅ Exported to {filepath}")
                    
                    with open(filepath, 'r') as f:
                        st.download_button(
                            label="⬇️ Download CSV",
                            data=f.read(),
                            file_name=os.path.basename(filepath),
                            mime="text/csv"
                        )
                except Exception as e:
                    st.error(f"Error exporting: {str(e)}")
        
        # Export leads only
        with col2:
            if st.button("🔥 Export Leads Only (CSV)", use_container_width=True):
                try:
                    filepath = exporter.export_to_leads_csv(results)
                    st.success(f"✅ Leads exported to {filepath}")
                    
                    with open(filepath, 'r') as f:
                        st.download_button(
                            label="⬇️ Download Leads",
                            data=f.read(),
                            file_name=os.path.basename(filepath),
                            mime="text/csv"
                        )
                except Exception as e:
                    st.error(f"Error exporting leads: {str(e)}")
        
        # Export summary report
        with col3:
            if st.button("📊 Generate Summary Report", use_container_width=True):
                try:
                    filepath = exporter.export_summary_report(results, city, state)
                    st.success(f"✅ Report generated: {filepath}")
                    
                    with open(filepath, 'r') as f:
                        st.download_button(
                            label="⬇️ Download Report",
                            data=f.read(),
                            file_name=os.path.basename(filepath),
                            mime="text/plain"
                        )
                except Exception as e:
                    st.error(f"Error generating report: {str(e)}")

else:
    # Show home screen
    st.info("👈 Use the sidebar to configure your scan and start searching for schools")

# ==================== Footer ====================
st.divider()
st.markdown("""
    ---
    **School Digital Gap Scanner** v1.0  
    Generate high-quality business leads for website development services
    
    💡 **How to use:**
    1. Enter city and state in the sidebar
    2. Adjust scan settings (optional)
    3. Click "Start Scanning"
    4. Review results and export leads
    
    📧 **Contact:** For API support or bulk scanning, contact our team
""")

logger.info("App session ended")
