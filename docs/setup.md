
cd cuisine_classifier
venv\Scripts\Activate
uvicorn cuisine_api:app --host 127.0.0.1 --port 8001 --reload

cd agents
cd menu_analyzer
venv\Scripts\Activate
uvicorn menu_analyzer_api:app --host 127.0.0.1 --port 8002 --reload 

cd agents
cd restaurant_finder
venv\Scripts\Activate
uvicorn restaurant_main:app --host 127.0.0.1 --port 8003 --reload

cd agents
cd recipe_recommender
venv\Scripts\Activate
uvicorn recipe_recommender_api:app --host 127.0.0.1 --port 8004 --reload

cd agents
cd spell_corrector
venv\Scripts\Activate
uvicorn spell_api:app --host 127.0.0.1 --port 8005 --reload

cd coordinator
cd src
venv\Scripts\Activate
cd ..
uvicorn src.coordinator_api:app --host 127.0.0.1 --port 8000 --reload

//ExecutionPolicy thing
Set-ExecutionPolicy RemoteSigned -Scope Process  

//Actual startup command
.\start_up.ps1