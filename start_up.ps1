# ==============================
# Start All Agents (PowerShell)
# ==============================

# Function to start a new PowerShell window for each agent
function Start-Agent {
    param (
        [string]$Path,
        [string]$VenvPath,
        [string]$Command
    )
    Start-Process powershell -ArgumentList "cd '$Path'; `$env:OPENROUTER_API_KEY='${env:OPENROUTER_API_KEY}'; `$env:OPENAI_BASE_URL='${env:OPENAI_BASE_URL}';`$env:LLM_MODEL='${env:LLM_MODEL}'; & '$VenvPath\Scripts\Activate.ps1'; $Command"
}

# --- 1. Cuisine Classifier Agent ---
Start-Agent -Path "agents\cuisine_classifier" `
             -VenvPath "venv" `
             -Command "uvicorn cuisine_api:app --host 127.0.0.1 --port 8001 --reload"

# --- 2. Menu Analyzer Agent ---
Start-Agent -Path "agents\menu_analyzer" `
             -VenvPath "venv" `
             -Command "uvicorn menu_analyzer_api:app --host 127.0.0.1 --port 8002 --reload"

# --- 3. Restaurant Finder Agent ---
Start-Agent -Path "agents\restaurant_finder" `
             -VenvPath "venv" `
             -Command "uvicorn restaurant_main:app --host 127.0.0.1 --port 8003 --reload"

# --- 4. Recipe Recommender Agent ---
Start-Agent -Path "agents\recipe_recommender" `
             -VenvPath "venv" `
             -Command "uvicorn recipe_recommender_api:app --host 127.0.0.1 --port 8004 --reload"

# --- 5. Spell Corrector Agent ---
Start-Agent -Path "agents\spell_corrector" `
             -VenvPath "venv" `
             -Command "uvicorn spell_api:app --host 127.0.0.1 --port 8005 --reload"

# --- 6. Spell Corrector Agent ---
Start-Agent -Path "agents\youtube_recipe_recommender" `
             -VenvPath "venv" `
             -Command "uvicorn youtube_api:app --host 127.0.0.1 --port 8006 --reload"

             
# --- 7. Coordinator ---
Start-Agent -Path "." `
             -VenvPath "coordinator\src\venv" `
             -Command "uvicorn coordinator.src.coordinator_api:app --host 127.0.0.1 --port 8000 --reload"
