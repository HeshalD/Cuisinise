# Cuisinise

 A multi-service, agentic food exploration platform that helps users find restaurants, analyze menus, classify cuisines, recommend recipes, and discover YouTube cooking videos. The system consists of a React frontend, a Node.js/Express backend, a Python FastAPI coordinator, and multiple specialized Python agent services.

 ---

 ## Quick Links

 - **Architecture**: `docs/architecture.md`
 - **Setup Guide**: `docs/setup.md`
 - **Roadmap**: `docs/roadmap.md`
 - **Startup Script (Windows)**: `start_up.ps1`

 ---

 ## Overview

 Cuisinise is composed of four major parts:

 - **Frontend (`frontend/`)**: React app (Create React App) that provides the UI.
 - **Backend (`backend/`)**: Node.js/Express API for auth, chat, and persistence (MongoDB via Mongoose).
 - **Coordinator (`coordinator/src/`)**: FastAPI service that orchestrates agent calls and formats results via an LLM.
 - **Agents (`agents/`)**: Independent FastAPI services for cuisine classification, menu analysis, restaurant search, recipe recommendations, spell correction, and YouTube recipe search.

 Default ports:

 - Frontend: `3000`
 - Backend: `5000`
 - Coordinator: `8000`
 - Agents: `8001`–`8006` (per agent; see below)

 ---

 ## Architecture (High-Level)

 - React frontend talks to the Express backend (`http://localhost:5000`).
 - Backend persists users, chats, and messages in MongoDB, and forwards user queries to the Coordinator.
 - Coordinator interprets user intent, builds a plan, calls relevant agents in parallel, and formats outputs with an LLM.
 - Backend stores the agent reply into the chat and returns it to the frontend.

 Key coordinator models (`coordinator/src/models.py`): `QueryRequest`, `Plan`, `CoordinatorResponse`.

 Agent service client contracts are defined in `coordinator/src/service_clients.py` and include:

 - `call_cuisine_predict()` → `CUISINE_BASE/predict`
 - `call_restaurant_search()` → `RESTAURANT_BASE/search`
 - `call_menu_analyze()` → `MENU_BASE/analyze`
 - `call_recipe_recommend()` → `RECIPE_BASE/recommend`
 - `call_youtube_search()` → `YOUTUBE_BASE/search_videos`
 - `call_spell_check()` / `send_spell_feedback()` → `SPELL_BASE` endpoints

 LLM formatting uses `OPENAI_API_KEY`/`OPENROUTER_API_KEY` and `LLM_MODEL`.

 ---

 ## Repository Structure

 - `frontend/` – React app (CRA). See `frontend/README.md` for CRA defaults.
 - `backend/` – Express API
   - `models/` – `User.js`, `Chat.js`, `Message.js`
   - `routes/` – `authRoutes.js`, `chatRoutes.js`
   - `middleware/` – `auth.js`
 - `coordinator/`
   - `src/` – FastAPI app, key files: `coordinator_api.py`, `service_clients.py`, `models.py`, router modules
 - `agents/`
   - `cuisine_classifier/` – `cuisine_api.py`, model artifacts (`*.pkl`)
   - `menu_analyzer/` – `menu_analyzer_api.py`, `main.py`
   - `restaurant_finder/` – `restaurant_main.py`/API entrypoint and helpers
   - `recipe_recommender/` – `recipe_recommender_api.py`, `models.py`
   - `spell_corrector/` – `spell_api.py`
   - `youtube_recipe_recommender/` – `youtube_api.py`
 - `docs/` – Architecture, roadmap, setup
 - `start_up.ps1` – Windows helper to launch all Python services in separate terminals

 ---

 ## Prerequisites

 - Node.js 18+
 - Python 3.10+ (3.11 recommended) with virtualenv
 - PowerShell (Windows) to run `start_up.ps1`
 - MongoDB Atlas project or accessible MongoDB instance

 ---

 ## Environment Variables

 The startup script forwards these to agent/coordinator shells. Set them in your PowerShell before running services:

 - `OPENROUTER_API_KEY`
 - `OPENAI_BASE_URL` (e.g., `https://openrouter.ai/api/v1`)
 - `LLM_MODEL` (e.g., `openrouter/<model>`)

 Backend uses `PORT` if provided (defaults to `5000`). JWT secret and MongoDB URI should be placed in `.env` (see Security), though current code may include a hardcoded MongoDB connection in `backend/app.js` per docs.

 Coordinator expects: `OPENAI_API_KEY`/`OPENROUTER_API_KEY`, `LLM_MODEL`, `*_BASE_URL` for agents, and optional `INTERNAL_TOKEN`.

 ---

 ## Installation

 From repository root:

 1) Frontend

 ```powershell
 npm --prefix frontend install
 ```

 2) Backend

 ```powershell
 npm --prefix backend install
 ```

 3) Python virtual environments (each agent + coordinator has its own venv expected by `start_up.ps1`)

 Example for one agent:

 ```powershell
 python -m venv agents/cuisine_classifier/venv
 agents/cuisine_classifier/venv/Scripts/Activate.ps1
 pip install -r agents/cuisine_classifier/requirements.txt
 Deactivate
 ```

 Repeat for:

 - `agents/menu_analyzer`
 - `agents/restaurant_finder`
 - `agents/recipe_recommender`
 - `agents/spell_corrector`
 - `agents/youtube_recipe_recommender` (if requirements are present)

 Coordinator venv:

 ```powershell
 python -m venv coordinator/src/venv
 coordinator/src/venv/Scripts/Activate.ps1
 pip install -r coordinator/src/requirements.txt
 Deactivate
 ```

 Notes:

 - ML-heavy agents may install large stacks (TensorFlow/PyTorch/spaCy/etc.). Ensure build tools/CUDA if needed, or prefer CPU wheels.
 - Root `requirements.txt` contains merge markers and appears unused; rely on per-service requirements.

 ---

 ## Running

 Option A — Start all Python services (agents + coordinator) via helper script:

 ```powershell
 ./start_up.ps1
 ```

 This launches:

 - Cuisine Classifier → `127.0.0.1:8001`
 - Menu Analyzer → `127.0.0.1:8002`
 - Restaurant Finder → `127.0.0.1:8003`
 - Recipe Recommender → `127.0.0.1:8004`
 - Spell Corrector → `127.0.0.1:8005`
 - YouTube Recipe Recommender → `127.0.0.1:8006`
 - Coordinator → `127.0.0.1:8000`

 Option B — Run individually:

 - Backend (Express):

 ```powershell
 npm --prefix backend start
 ```

 - Frontend (React):

 ```powershell
 npm --prefix frontend start
 ```

 - Agents/Coordinator (uvicorn) — see `start_up.ps1` for exact commands. Example:

 ```powershell
 agents/cuisine_classifier/venv/Scripts/Activate.ps1
 uvicorn cuisine_api:app --host 127.0.0.1 --port 8001 --reload

 coordinator/src/venv/Scripts/Activate.ps1
 uvicorn coordinator.src.coordinator_api:app --host 127.0.0.1 --port 8000 --reload
 ```

 ---

 ## Backend API (Selected Endpoints)

 - `POST /api/auth/register` — Register user
 - `POST /api/auth/login` — JWT login
 - `DELETE /api/auth/account` — Delete account (auth)
 - `POST /api/chats` — Create chat (auth)
 - `GET /api/chats` — List chats (auth)
 - `GET /api/chats/:chatId/messages` — List messages (auth)
 - `POST /api/chats/:chatId/messages` — Add user message, trigger Coordinator, save agent reply (auth)
 - `POST /api/chats/:chatId/summary` — Recompute summary (auth)
 - `GET /api/chats/:chatId/summary` — Get summary (auth)
 - `DELETE /api/chats/:chatId` — Delete chat (auth)

 Middleware: `backend/middleware/auth.js` reads `Authorization: Bearer <token>` and sets `req.userId`.

 CORS: configured for `http://localhost:3000` in development.

 ---

 ## Coordinator API (Selected Endpoints)

 - `GET /health` — Health check
 - `POST /generate-title` — Generate chat title from first message
 - `POST /query` — Orchestrate agent calls based on inferred plan and return aggregated results

 Coordinator logic:

 - Spell checks input
 - Extracts location, price, cuisine, detects intents: `find_restaurant`, `recommend_recipe`, `analyze_menu`, fallback `classify_cuisine`
 - Calls appropriate agents in parallel
 - Formats results via LLM into a friendly `formatted_summary`

 ---

 ## Agent Services

 Each agent is an independent FastAPI module with its own `requirements.txt` and uvicorn entrypoint.

 - `agents/cuisine_classifier/` — `POST /predict { text } → { cuisine }`
 - `agents/menu_analyzer/` — `POST /analyze { text } → nutrition/insights`
 - `agents/restaurant_finder/` — `POST /search { cuisine, location, price, min_rating, top_k } → restaurants`
 - `agents/recipe_recommender/` — `POST /recommend { query, top_k } → recipes`
 - `agents/spell_corrector/` — `POST /check`, `POST /feedback`
 - `agents/youtube_recipe_recommender/` — `POST /search_videos { recipe_name, top_k } → videos`

 Base URLs are configured via environment variables (`*_BASE_URL`) and optionally secured by `X-Internal-Token`.

 ---

 ## Security

 - Use JWT for backend auth; send `Authorization: Bearer <token>`.
 - Configure CORS narrowly for production on both Backend and Coordinator.
 - Move secrets to `.env` files and never commit real credentials. Recommended vars:
   - Backend: `JWT_SECRET`, `MONGODB_URI`, `PORT`, `FASTAPI_URL`
   - Coordinator: `OPENAI_API_KEY` or `OPENROUTER_API_KEY`, `LLM_MODEL`, agent `*_BASE_URL`, `INTERNAL_TOKEN`

 Note: Docs indicate a hardcoded MongoDB connection in `backend/app.js`; plan to replace with `MONGODB_URI` from `.env`.

 ---

 ## Troubleshooting

 - Python installs fail: ensure venv activated; install MSVC Build Tools; prefer CPU wheels if GPU/CUDA unavailable.
 - Frontend cannot call backend: verify backend on `5000` and CORS origin `http://localhost:3000`.
 - LLM credentials not found: export `OPENROUTER_API_KEY`, `OPENAI_BASE_URL`, `LLM_MODEL` before launching services.
 - Root `requirements.txt` has merge markers; ignore in favor of per-service requirements.

 ---

 ## Roadmap (Summary)

 - Phase 1: Agents — implemented
 - Phase 2: Coordinator — implemented
 - Phase 3: Backend — implemented
 - Phase 4: Frontend — implemented
 - Phase 5: Dockerization — planned (Dockerfiles and docker-compose to be added)
 - Phase 6: Deployment — planned (CI/CD, secret management, hosting)

 See `docs/roadmap.md` for details.

 ---

 ## Contributing

 - Use separate terminals for frontend, backend, and each Python service.
 - Keep venv paths as referenced by `start_up.ps1` to avoid modifying the script.
 - Consider adding structured logging and metrics (timings, errors) to Coordinator and agents.

 ---

 ## License

 Specify license terms here (e.g., MIT). If absent, the project is not licensed for public reuse by default.