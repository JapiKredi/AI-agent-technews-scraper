#!/bin/bash

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install python-dotenv pydantic streamlit beautifulsoup4 requests groq pandas aiohttp

# Save requirements
pip freeze > requirements.txt

# Create project files
touch .env
touch main.py
touch config.py
touch models.py
touch scraper.py

# Create .gitignore
echo "venv/
__pycache__/
.env
.idea/
.vscode/
*.pyc
.DS_Store" > .gitignore

# Create basic .env template
echo "GROQ_API_KEY=your_groq_api_key_here" > .env

echo "Setup complete! Don't forget to:"
echo "1. Activate your virtual environment: source venv/bin/activate"
echo "2. Add your GROQ API key to .env"
echo "3. Run the app: streamlit run main.py"