# agents/coordinator/coordinator_api.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import asyncio

from .models import QueryRequest, CoordinatorResponse
from .router import plan_from_query
from .service_clients import (
    call_cuisine_predict, call_restaurant_search,
    call_menu_analyze, call_recipe_recommend,
    call_spell_check, send_spell_feedback
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
    # 0) Spell check pre-processing
    spell_meta = {
        "spell_checked": False,
        "original_query": req.query,
        "corrected_query": None,
        "correction_confidence": None,
        "correction_candidates": None,
    }
    spell_error = None
    try:
        spell = await call_spell_check(req.query, req.user_id, top_k=3)
        spell_meta["spell_checked"] = True
        spell_meta["corrected_query"] = spell.get("corrected")
        spell_meta["correction_candidates"] = spell.get("candidates")
        # crude confidence: top candidate score if present
        cands = spell.get("candidates") or []
        if cands:
            spell_meta["correction_confidence"] = float(cands[0].get("score", 0.0))
        # If changed and not auto-accept, return suggestion for confirmation
        if spell.get("changed") and not req.auto_accept_spell:
            return CoordinatorResponse(
                plan=None,  # no plan yet; waiting for user confirmation
                results={"message": "Did you mean...?"},
                **spell_meta
            )
        # Auto-accept path or unchanged
        if spell.get("changed") and req.auto_accept_spell:
            # record positive feedback for auto-accept
            try:
                await send_spell_feedback(req.query, spell.get("corrected"), True, req.user_id)
            except Exception:
                pass
            req.query = spell.get("corrected")
    except Exception as e:
        # proceed without spell correction on failure; log for diagnosis
        spell_error = str(e)
        try:
            print(f"[WARN] Spell check failed: {spell_error}")
        except Exception:
            pass

    # 1) Parse query → plan using possibly corrected query
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

    if spell_error:
        results["spell_error"] = spell_error
    return CoordinatorResponse(plan=plan, results=results, **spell_meta)

async def _wrap(key: str, coro):
    try:
        data = await coro
        return key, data
    except Exception as e:
        return key, e
