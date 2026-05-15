# 🚀 Local Testing Guide

## ✅ First Time Setup
```bash
# 1. Navigate to project folder
cd "h:\Ai product\route-explorer"

# 2. Verify config
python test_config.py

# Should show: ✅ All required keys are configured!
```

---

## 🎯 Run App (Choose One)

### Option 1️⃣: PowerShell (Recommended - Easiest!)
```powershell
# Direct command
& "C:/Program Files/Python313/python.exe" -m streamlit run app.py

# OR use the script
.\start.ps1
```

### Option 2️⃣: Command Prompt (CMD)
```cmd
# Direct command
"C:\Program Files\Python313\python.exe" -m streamlit run app.py

# OR double-click start.bat
```

### Option 3️⃣: Git Bash
```bash
"/c/Program Files/Python313/python.exe" -m streamlit run app.py
```

---

## 🌐 Access App
- **Local**: http://localhost:8501
- App browser automatically khul jayega
- Agar nahi khula toh manually copy-paste karo

---

## 📋 How to Use App

1. **From**: शहर का नाम (e.g., Shimla)
2. **To**: Destination (e.g., Paonta Sahib)  
3. **What to find**: खोजने की चीज़ (e.g., plant nurseries)
4. **Click**: "🔍 Search Route & Places"

App यह करेगा:
```
Your Input
    ↓
Coordinates निकाले (Google Geocoding)
    ↓
OpenRouteService से route लेगा
    ↓
Route पर waypoints निकाले
    ↓
Ollama AI से query बनवाएगा
    ↓
Results दिखाएगा
```

---

## ⚙️ Requirements Check

### Ollama चाहिए!
```bash
# अगर Ollama नहीं है तो:
# 1. Download करो: https://ollama.ai
# 2. Install करो
# 3. यह command चलाओ:
ollama serve
ollama pull mistral

# दूसरे terminal में app चलाओ
```

### Internet चाहिए
- ✅ Route API calls के लिए
- ✅ Geocoding के लिए
- ❌ Ollama के लिए नहीं (local है)

---

## 🐛 अगर Error आए

| Error | Solution |
|-------|----------|
| `No module named 'dotenv'` | `pip install -r requirements.txt` |
| `Port 8501 already in use` | App पहले से चल रहा है, बंद करो या port बदल: `streamlit run app.py --server.port 8502` |
| `OpenRouteService error` | Internet check करो, API key .env में है? |
| `Ollama not running` | Ollama start करो (separate terminal में `ollama serve`) |

---

## ✨ Quick Start (अभी करो!)

```powershell
cd "h:\Ai product\route-explorer"
& "C:/Program Files/Python313/python.exe" -m streamlit run app.py
```

**Done!** App browser में खुल जाएगा 🎉
