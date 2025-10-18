# Cuisinise — Setup Guide

## Overview
Cuisinise is a multi-service project with:
- *Frontend* frontend/ (React, runs on port 3000).
- *Backend* backend/ (Express, default port 5000).
- *Coordinator* coordinator/src/ (FastAPI, port 8000).
- *Agents* under agents/ (FastAPI/uvicorn services):
  - cuisine_classifier → 127.0.0.1:8001
  - menu_analyzer → 127.0.0.1:8002
  - restaurant_finder → 127.0.0.1:8003
  - recipe_recommender → 127.0.0.1:8004
  - spell_corrector → 127.0.0.1:8005
  - youtube_recipe_recommender → 127.0.0.1:8006 (folder present; requirements file not found)

A helper script start_up.ps1 can launch all Python services in separate PowerShell windows.

## Prerequisites
- Node.js 18+ and npm
- Python 3.10+ (recommend 3.11) with venv
- PowerShell (for Windows) to run start_up.ps1
- MongoDB Atlas project or accessible MongoDB

## Environment Variables
The PowerShell launcher forwards these from your current environment to all agent/coordinator shells:
- OPENROUTER_API_KEY
- OPENAI_BASE_URL
- LLM_MODEL

Set them in your current shell before running the startup script. Example (PowerShell):
powershell
$env:OPENROUTER_API_KEY = "<your_key>"
$env:OPENAI_BASE_URL = "https://openrouter.ai/api/v1" # or your base URL
$env:LLM_MODEL = "openrouter/<model-name>"


Backend reads .env via dotenv and uses PORT if set; otherwise defaults to 5000. The MongoDB URI is currently hardcoded in backend/app.js and not read from env.

## Install

### 1) Frontend
powershell
# from repo root
npm --prefix frontend install


### 2) Backend
powershell
npm --prefix backend install


### 3) Python virtual environments
The startup script expects a venv named venv in each agent folder, and coordinator/src/venv for the coordinator.

Create and install dependencies for each:
powershell
# Cuisine Classifier
python -m venv agents/cuisine_classifier/venv
agents/cuisine_classifier/venv/Scripts/Activate.ps1
pip install -r agents/cuisine_classifier/requirements.txt
Deactivate

# Menu Analyzer
python -m venv agents/menu_analyzer/venv
agents/menu_analyzer/venv/Scripts/Activate.ps1
pip install -r agents/menu_analyzer/requirements.txt
Deactivate

# Restaurant Finder
python -m venv agents/restaurant_finder/venv
agents/restaurant_finder/venv/Scripts/Activate.ps1
pip install -r agents/restaurant_finder/requirements.txt
Deactivate

# Recipe Recommender
python -m venv agents/recipe_recommender/venv
agents/recipe_recommender/venv/Scripts/Activate.ps1
pip install -r agents/recipe_recommender/requirements.txt
Deactivate

# Spell Corrector
python -m venv agents/spell_corrector/venv
agents/spell_corrector/venv/Scripts/Activate.ps1
pip install -r agents/spell_corrector/requirements.txt
Deactivate

# (Optional) YouTube Recipe Recommender
# Folder exists but requirements.txt not found; create venv and install manually if needed.
python -m venv agents/youtube_recipe_recommender/venv

# Coordinator
python -m venv coordinator/src/venv
coordinator/src/venv/Scripts/Activate.ps1
pip install -r coordinator/src/requirements.txt
Deactivate


Notes:
- Some agents install large ML stacks (TensorFlow, PyTorch, spaCy, transformers). Installation may take time and may require Build Tools/CUDA as appropriate.
- agents/recipe_recommender/requirements.txt includes a direct URL for en_core_web_md; pip installs it automatically.

## Run

### Option A: Run everything (agents + coordinator) via PowerShell helper
From the repository root:
powershell
./start_up.ps1

This opens multiple PowerShell windows, each running one service:
- cuisine_classifier on 127.0.0.1:8001
- menu_analyzer on 127.0.0.1:8002
- restaurant_finder on 127.0.0.1:8003
- recipe_recommender on 127.0.0.1:8004
- spell_corrector on 127.0.0.1:8005
- youtube_recipe_recommender on 127.0.0.1:8006 (if code present)
- coordinator on 127.0.0.1:8000

### Option B: Run services individually

- Backend (Express):
powershell
npm --prefix backend start

Defaults to port 5000 unless PORT is set. CORS is configured for http://localhost:3000.

- Frontend (React):
powershell
npm --prefix frontend start

Served at http://localhost:3000.

- Agents/Coordinator (uvicorn):
Use the exact commands defined in start_up.ps1 (they include host, port, and module):
powershell
# examples
# 8001
agents/cuisine_classifier/venv/Scripts/Activate.ps1
uvicorn cuisine_api:app --host 127.0.0.1 --port 8001 --reload

# 8000 (coordinator)
coordinator/src/venv/Scripts/Activate.ps1
uvicorn coordinator.src.coordinator_api:app --host 127.0.0.1 --port 8000 --reload


## Configuration Details
- Backend server: backend/app.js
  - Port: process.env.PORT || 5000
  - MongoDB connection (currently hardcoded):
    js
    mongoose.connect('mongodb+srv://Heshal:12345@cuisinise.swojida.mongodb.net/');
    
  - Routes: "/api/auth", "/api/chats"
- Frontend: frontend/package.json scripts use react-scripts.
- Coordinator/Agents: uvicorn apps per agent with their own requirements and ports.

## Common Issues
- If Python installs fail:
  - Ensure you activated the correct venv before pip install.
  - Install Microsoft C++ Build Tools for packages with native extensions.
  - For GPU extras (e.g., torch with CUDA), verify CUDA toolkit compatibility or switch to CPU wheels.
- If frontend cannot call backend:
  - Confirm backend on port 5000 and CORS origin http://localhost:3000.
  - Update CORS in backend/app.js if using a different frontend URL.
- If services cannot find LLM credentials:
  - Export OPENROUTER_API_KEY, OPENAI_BASE_URL, and LLM_MODEL in the shell before launching.
- requirements.txt at repo root contains merge conflict markers and appears unused by services. Resolve or ignore.

## Development Tips
- Use separate terminals for frontend, backend, and Python services.
- Keep virtualenvs as referenced by start_up.ps1 to avoid path edits.
- Consider moving secrets (MongoDB URI, JWT secrets) into .env files and reading them via dotenv.