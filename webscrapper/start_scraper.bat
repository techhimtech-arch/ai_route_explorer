@echo off
REM Start Web Scraper App
echo.
echo ===================================
echo   Web Scraper App - Starting...
echo ===================================
echo.

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Check if dependencies are installed
echo Installing/Checking dependencies...
pip install -r requirements.txt --quiet

REM Start the app
echo.
echo Starting Web Scraper App...
echo Open your browser to: http://localhost:8501
echo.
streamlit run scraper_app.py

pause
