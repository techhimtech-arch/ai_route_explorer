# 🔍 Web Scraper App - Setup & Deployment Guide

## ✨ Features

- **Simple Search** - No location parameters needed
- **Multiple Sources** - Google, Wikipedia, DuckDuckGo
- **Business Finder** - Find restaurants, stores, services
- **Export Data** - Download results as CSV/JSON
- **No API Keys** - Completely free!

---

## 🚀 Quick Start (Local)

### Step 1: Install New Dependencies
```bash
# First update requirements
pip install -r requirements.txt

# Or just install the new libraries:
pip install beautifulsoup4==4.12.2 pandas==2.1.3
```

### Step 2: Run the Scraper App
```bash
streamlit run scraper_app.py
```

Open your browser to: `http://localhost:8501`

---

## 📊 How to Use

1. **Enter Search Query**: Type anything you want to find
   - "Restaurants in Karachi"
   - "Apple stores"
   - "Python tutorials"
   - "Pizza delivery near me"

2. **Choose Search Type**:
   - 📍 Businesses/Places
   - 🏢 Companies
   - 📰 News
   - 🛍️ Products

3. **Click Search** - Results appear instantly!

4. **Export Results** - Save as CSV/JSON

---

## 🌍 Deploy to Streamlit Cloud (FREE!)

### Step 1: Prepare Files for Deployment

Your current files are ready! You just need:
- ✅ `scraper_app.py` - Main app
- ✅ `requirements.txt` - Updated with scraping libs
- ✅ No .env file needed for scraper (no API keys!)

### Step 2: Push to GitHub

```bash
cd h:\Ai\ product\route-explorer

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Add web scraper app"

# Push to GitHub
git push origin main
```

### Step 3: Deploy on Streamlit Cloud

1. Go to: https://streamlit.io/cloud
2. Sign up with GitHub account
3. Click "New app"
4. Select your repository
5. Select branch: `main`
6. Main file path: `scraper_app.py`
7. Click "Deploy"

**✅ Done! Your app is live!**

---

## 🔧 Environment & Other Deployment Options

### Option 1: Railway.app (Paid but Easy)
```bash
# Create account at railway.app
# Push code to GitHub
# Connect Railway to GitHub repo
# Deploy in 2 clicks
```

### Option 2: Replit (Free)
```bash
# Go to replit.com
# Create new Replit project
# Paste your code
# Click "Run"
```

### Option 3: Hugging Face Spaces (Free)
```bash
# Go to huggingface.co/spaces
# Create new Space
# Upload files or connect GitHub
# Deploy instantly
```

### Option 4: Heroku (Free tier deprecated, but budget option)
```bash
# Use Railway or Render instead
```

---

## 📝 Differences Between Apps

### Route Explorer App (`app.py`)
- ✅ Find businesses ALONG routes
- ✅ Needs: Start location, End location, Search type
- ✅ Uses: OpenRouteService API + Ollama AI
- ✅ More powerful but needs setup

### Web Scraper App (`scraper_app.py`)
- ✅ Find ANYTHING online
- ✅ Just needs: Search query
- ✅ No dependencies or API keys
- ✅ Deploy anywhere instantly
- ✅ Perfect for quick searches

---

## 🛠️ Running Both Apps

You can run BOTH apps in the same workspace:

```bash
# Terminal 1 - Route Explorer
streamlit run app.py --logger.level=info

# Terminal 2 - Web Scraper
streamlit run scraper_app.py
```

They'll run on different ports:
- Route Explorer: `http://localhost:8501`
- Web Scraper: `http://localhost:8502`

---

## 🐛 Troubleshooting

### Issue: "No module named beautifulsoup4"
**Solution:**
```bash
pip install beautifulsoup4
```

### Issue: Search results are empty
**Solution:**
- Try a simpler search term
- Try different search type
- Check internet connection
- Try again (rate limit may apply)

### Issue: App won't start
**Solution:**
```bash
# Check dependencies
pip install -r requirements.txt

# Try running with verbose output
streamlit run scraper_app.py --logger.level=debug
```

### Issue: Deploy fails on Streamlit Cloud
**Solution:**
1. Make sure `requirements.txt` is in root folder
2. No .env file needed for scraper
3. Try deploying from main branch
4. Check logs in Streamlit Cloud console

---

## 📤 Recommended Deployment (BEST OPTION)

**Streamlit Cloud** ✨
- Free tier available
- Deploy from GitHub
- Custom domain support
- 1-click deploy
- Best performance

**Steps:**
1. Push code to GitHub
2. Go to streamlit.io/cloud
3. Select repo + file
4. Click Deploy

Done! 🎉

---

## 💡 Future Improvements

Ideas to make it better:
- Add caching for faster results
- Save search history
- Add filters (price, rating, etc.)
- Email search results
- Schedule searches
- Database integration
- User authentication

---

**Happy Scraping! 🔍**

Need help? Check `COMMANDS.md` for more commands.
