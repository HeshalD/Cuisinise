# agents/coordinator/coordinator_api.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import asyncio

from .models import QueryRequest, CoordinatorResponse
from .router import plan_from_query
from .service_clients import (
    call_cuisine_predict, call_restaurant_search,
    call_menu_analyze, call_recipe_recommend
)

app = FastAPI(title="Food Explorer Coordinator")

# (optional) allow your web UI to call this service
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/query", response_model=CoordinatorResponse)
async def handle_query(req: QueryRequest):
    # 1) Parse query → plan
    plan = plan_from_query(req.query, req.location, req.top_k)

    results = {}

    # 2) Possibly classify cuisine first if needed
    cuisine = plan.cuisine
    if "classify_cuisine" in plan.intents and not cuisine:
        try:
            cuisine = await call_cuisine_predict(req.query)
            plan.cuisine = cuisine
        except Exception as e:
            # non-fatal; continue with other intents
            results["classifier_error"] = str(e)

    # 3) Build tasks based on intents
    tasks = []

    if "find_restaurant" in plan.intents:
        tasks.append(_wrap("restaurants", call_restaurant_search(
            cuisine=plan.cuisine,
            location=plan.location,
            price=plan.price,
            min_rating=plan.min_rating or 0,
            top_k=plan.top_k
        )))

    if "analyze_menu" in plan.intents:
        tasks.append(_wrap("menu_analysis", call_menu_analyze(req.query)))

    if "recommend_recipe" in plan.intents:
        tasks.append(_wrap("recipes", call_recipe_recommend(
            query=req.query,
            top_k=plan.top_k
        )))

    # 4) Execute in parallel
    if tasks:
        done = await asyncio.gather(*tasks, return_exceptions=True)
        for key, payload in done:
            if isinstance(payload, Exception):
                results[f"{key}_error"] = str(payload)
            else:
                results[key] = payload

    return CoordinatorResponse(plan=plan, results=results)

async def _wrap(key: str, coro):
    try:
        data = await coro
        return key, data
    except Exception as e:
        return key, e
