# Start Web Scraper App

Write-Host ""
Write-Host "===================================" -ForegroundColor Cyan
Write-Host "  Web Scraper App - Starting..." -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment
& ".\.venv\Scripts\Activate.ps1"

# Check if dependencies are installed
Write-Host "Installing/Checking dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet

# Start the app
Write-Host ""
Write-Host "Starting Web Scraper App..." -ForegroundColor Green
Write-Host "Open your browser to: http://localhost:8501" -ForegroundColor Green
Write-Host ""

streamlit run scraper_app.py
