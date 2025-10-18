# Cuisinise Architecture

## Overview

Cuisinise is a multi-service, agentic food exploration platform. It consists of a React web frontend, a Node.js/Express API backend with MongoDB for auth and chat persistence, and a Python FastAPI coordinator that orchestrates specialized agent services (cuisine classification, restaurant search, menu analysis, recipe recommendations, YouTube search, and spell correction).

## High-Level Components

- **Frontend (frontend/)**
- **Backend API (backend/)**
- **Coordinator API (coordinator/src/)**
- **Agent Services (agents/)**
- **Shared Assets and Docs (docs/, README.md)**

## Frontend (frontend/)

- React (Create React App) per frontend/package.json.
- Talks to Backend at http://localhost:5000 for auth and chat operations.
- Receives formatted agent responses via Backend which proxies to Coordinator.

## Backend API (backend/)

- Express app in backend/app.js.
- MongoDB via Mongoose models:
  - backend/models/User.js (email, passwordHash, comparePassword)
  - backend/models/Chat.js (title, summary, timestamps)
  - backend/models/Message.js (chatId, role=user|agent, text)
- Routes:
  - backend/routes/authRoutes.js
    - POST /api/auth/register — create user
    - POST /api/auth/login — JWT login
    - DELETE /api/auth/account — delete account (auth)
  - backend/routes/chatRoutes.js
    - POST /api/chats — create chat (auth)
    - GET /api/chats — list chats (auth)
    - GET /api/chats/:chatId/messages — list messages (auth)
    - POST /api/chats/:chatId/messages — add user message, call Coordinator, save agent reply (auth)
    - POST /api/chats/:chatId/summary — recompute summary (auth)
    - GET /api/chats/:chatId/summary — get summary (auth)
    - DELETE /api/chats/:chatId — delete chat (auth)
- Middleware:
  - backend/middleware/auth.js — JWT bearer parsing, sets req.userId.
- External dependencies:
  - CORS set to http://localhost:3000.
  - MongoDB connection: mongoose.connect('mongodb+srv://...') in app.js.
  - Coordinator URL: FASTAPI_URL env var (default http://localhost:8000).

## Coordinator API (coordinator/src/)

- FastAPI app in coordinator/src/coordinator_api.py.
- Key models in coordinator/src/models.py:
  - QueryRequest (query, location, top_k, user_id, history, summary)
  - Plan (intents, cuisine, location, price, min_rating, top_k)
  - CoordinatorResponse (plan, results, spell-check metadata)
- Router in coordinator/src/router.py:
  - Extracts location, price, cuisine, and detects intents: find_restaurant, recommend_recipe, analyze_menu, or fallback classify_cuisine.
  - Builds a Plan from user query.
- Service clients in coordinator/src/service_clients.py (async httpx):
  - call_cuisine_predict() → CUISINE_BASE/predict
  - call_restaurant_search() → RESTAURANT_BASE/search
  - call_menu_analyze() → MENU_BASE/analyze
  - call_recipe_recommend() → RECIPE_BASE/recommend
  - call_youtube_search() → YOUTUBE_BASE/search_videos
  - call_spell_check() / send_spell_feedback() → SPELL_BASE endpoints
  - Base URLs via env: *_BASE_URL, optional X-Internal-Token header
- LLM formatting:
  - Uses openai.OpenAI client with LLM_MODEL to generate a friendly formatted_summary of raw results.
- Endpoints:
  - GET /health
  - POST /generate-title — generate chat title from first message
  - POST /query — orchestrate plan execution and return aggregated results

## Agent Services (agents/)

Each agent is an independent Python service/module with its own requirements.txt and API module:

- agents/cuisine_classifier/
  - cuisine_api.py, cuisine_classifier.py, model artifacts (*.pkl)
  - Endpoint (expected): POST /predict { text } → { cuisine }
- agents/menu_analyzer/
  - menu_analyzer_api.py, menu_analyzer.py
  - Endpoint (expected): POST /analyze { text } → nutrition/insights
- agents/recipe_recommender/
  - recipe_recommender_api.py, search.py, GPU helpers
  - Endpoint (expected): POST /recommend { query, top_k } → recipes
- agents/restaurant_finder/
  - restaurant_api.py, restaurant_data.py
  - Endpoint (expected): POST /search { cuisine, location, price, min_rating, top_k } → restaurants
- agents/spell_corrector/
  - spell_api.py, large domain vocabulary and embeddings
  - Endpoints (expected): POST /check, POST /feedback
- agents/youtube_recipe_recommender/
  - youtube_api.py, gpu_optimizer.py
  - Endpoint (expected): POST /search_videos { recipe_name, top_k } → videos

Note: Agent APIs are inferred from coordinator/src/service_clients.py contract and code references.

## Data Flow

1. User interacts with the React app (frontend/).
2. Frontend calls Backend (backend/app.js) for auth and chat operations.
3. When posting a message (POST /api/chats/:chatId/messages), Backend:
   - Saves user Message.
   - Optionally sets chat title via POST {FASTAPI_URL}/generate-title.
   - Sends QueryRequest to Coordinator POST /query with history and summary.
4. Coordinator (/query):
   - Spell checks input.
   - Builds Plan from query.
   - Calls agent services in parallel based on Plan.
   - Formats results via LLM into formatted_summary.
5. Backend saves agent Message and updates Chat.lastActivityAt.
6. Periodically updates Chat.summary via POST {FASTAPI_URL}/summarize from chatRoutes.js.

## Environment and Configuration

- Backend: JWT_SECRET, FASTAPI_URL, MongoDB URI (currently hardcoded in app.js).
- Coordinator: OPENAI_API_KEY/OPENROUTER_API_KEY, LLM_MODEL, *_BASE_URL for agents, INTERNAL_TOKEN.
- Agents: each service may require its own API keys or model assets as per its requirements.txt and modules.

## Ports (defaults)

- Frontend: 3000
- Backend: 5000
- Coordinator: 8000
- Agents (inferred defaults from service_clients.py):
  - Cuisine: 8001
  - Menu Analyzer: 8002
  - Restaurant Finder: 8003
  - Recipe Recommender: 8004
  - Spell Corrector: 8005
  - YouTube Search: 8006

## Security Considerations

- Backend JWT via Authorization: Bearer <token> (backend/middleware/auth.js).
- Optional internal token for service-to-service calls: X-Internal-Token.
- Configure CORS tightly in production on both Backend and Coordinator.

## Persistence

- MongoDB stores users, chats, and messages via Mongoose schemas.
- Summaries stored on Chat.summary and updated periodically.

## Observability

- Coordinator logs debug info for service calls (payloads, statuses) in service_clients.py.
- Consider adding structured logging and metrics (request timings, errors) later.