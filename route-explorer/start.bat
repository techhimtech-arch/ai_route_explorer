@echo off
REM AI Route Explorer - Start Script for CMD/PowerShell
REM Ek click se app chal jayega

echo.
echo ========================================
echo   🚀 AI Route Explorer
echo ========================================
echo.

REM Check if .env exists
if not exist ".env" (
    echo ❌ .env file not found!
    echo 💡 Pehle .env file banao ya .env.example copy karo
    pause
    exit /b 1
)

echo ⏳ Starting app...
echo.

REM Run streamlit
"C:\Program Files\Python313\python.exe" -m streamlit run app.py

REM Agar app close ho jaye
echo.
echo 👋 App closed
pause
