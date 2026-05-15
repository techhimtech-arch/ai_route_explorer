# AI Route Explorer - Start Script for PowerShell
# Ek click se app chal jayega

Write-Host "🚀 Starting AI Route Explorer..." -ForegroundColor Green
Write-Host "⏳ Wait karo..." -ForegroundColor Yellow
Write-Host ""

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "❌ .env file not found!" -ForegroundColor Red
    Write-Host "💡 Pehle .env file banao ya .env.example copy karo" -ForegroundColor Yellow
    exit 1
}

# Run streamlit with proper Python path
& "C:/Program Files/Python313/python.exe" -m streamlit run app.py --logger.level=info

# Agar app close ho jaye
Write-Host ""
Write-Host "👋 App closed" -ForegroundColor Yellow
