# Route Explorer - Local Development Commands

## Setup
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

pip install -r requirements.txt

## Start Ollama (in separate terminal)
ollama serve
ollama pull mistral  # First time only

## Run the App
streamlit run app.py

## Testing
python -m pytest tests/  # When tests are added

## Format Code
black services/ utils/

## Lint Code
pylint services/ utils/

## Build & Deploy
# Will add deployment commands here
