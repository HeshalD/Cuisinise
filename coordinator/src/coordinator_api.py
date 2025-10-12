# agents/coordinator/coordinator_api.py
from openai import OpenAI
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import os
from dotenv import load_dotenv
from typing import List, Optional
from pydantic import BaseModel

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

from .models import QueryRequest, CoordinatorResponse, HistoryMessage
from .router import plan_from_query
from .service_clients import (
    call_cuisine_predict, call_restaurant_search,
    call_menu_analyze, call_recipe_recommend,
    call_spell_check, send_spell_feedback,
    call_youtube_search
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

class TitleRequest(BaseModel):
    query: str

@app.post("/generate-title")
async def generate_title(req: TitleRequest):
    """
    Generate a concise chat title (3-6 words) from the first user message using the same LLM client.
    """
    prompt = (
        "Generate a concise chat title (3-6 words) based on this first user message. "
        "Use sentence case. Do not include quotes or trailing punctuation.\n\n"
        f"Message: {req.query}\n"
        "Title:"
    )

    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[
                {"role": "system", "content": "You generate short, descriptive chat titles. 3-6 words, sentence case, no trailing punctuation."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.4,
            extra_headers={
                "HTTP-Referer": os.getenv("OPENROUTER_SITE_URL", ""),
                "X-Title": os.getenv("OPENROUTER_SITE_NAME", ""),
            },
        )
        title = (response.choices[0].message.content or "").strip()
        if "\n" in title:
            title = title.splitlines()[0].strip()
        title = title.strip('"').strip("'")
        if len(title) > 60:
            title = title[:60].rstrip()
        if not title:
            title = "New Chat"
        return {"title": title}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Title generation failed: {str(e)}")

@app.post("/query", response_model=CoordinatorResponse)
async def handle_query(req: QueryRequest):
    print(f"[Coordinator] Received query: {req.query}")
    print(f"[Coordinator] Context length: {len(req.history)}")
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
        # Always auto-apply corrections when changed; otherwise proceed as-is
        if spell.get("changed"):
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
        # Also fetch related YouTube videos for the recipe query
        tasks.append(_wrap("youtube_videos", call_youtube_search(
            recipe_name=req.query,
            top_k=plan.top_k
        )))

    # 4) Execute in parallel
    if tasks:
        done = await asyncio.gather(*tasks, return_exceptions=True)
        for key, payload in done:
            if isinstance(payload, Exception):
                # Ensure we never return an empty error message
                msg = str(payload)
                if not msg:
                    msg = f"{type(payload).__name__}: {repr(payload)}"
                results[f"{key}_error"] = msg
            else:
                results[key] = payload

    try:
        formatted_summary = await format_results_with_llm(req.query, plan, results, req.history or [])
        results["formatted_summary"] = formatted_summary
    except Exception as e:
        results["llm_format_error"] = str(e)

    if spell_error:
        results["spell_error"] = spell_error
    return CoordinatorResponse(plan=plan, results=results, **spell_meta)

async def _wrap(key: str, coro):
    try:
        data = await coro
        return key, data
    except Exception as e:
        return key, e

async def format_results_with_llm(query: str, plan, results: dict, history: list):
    """
    Uses an OpenAI LLM to summarize and format messy multi-agent results
    into structured, human-readable text.
    """

    context_text = ""
    if history:
        context_text = "\n".join(
            [f"{m.role.capitalize()}: {m.text}" for m in history[-10:]]
        )

    # Prepare the prompt
    prompt = f"""
You are the "Food Explorer" AI assistant. You receive raw outputs from several specialized agents:
- Cuisine classifier
- Restaurant finder
- Menu analyzer
- Recipe recommender
- YouTube video searcher
- Spell checker

Conversation so far:
{context_text}

Your task:
- Combine and summarize the data clearly.
- Present it in readable form for a user.
- Use headings and bullet points.
- If an agent failed, note it briefly.
- Include restaurant names, cuisines, menu insights, recipes, and video titles if available.
-Respond naturally as if continuing the conversation.
-Keep it contextual, concise, and friendly.

---

**User Query:** {query}

**Interpreted Plan:**
{plan.model_dump_json(indent=2)}

**Raw Results:**
{results}

---

Now create a concise, readable response for the user:
"""

    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o",  # OpenRouter model route
            messages=[
                {"role": "system", "content": "You are a helpful and organized summarization assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.6,
            extra_headers={
                "HTTP-Referer": os.getenv("OPENROUTER_SITE_URL", ""),
                "X-Title": os.getenv("OPENROUTER_SITE_NAME", ""),
            },
        )
        formatted = response.choices[0].message.content
        return formatted
    except Exception as e:
        return f"[LLM Formatting Error: {str(e)}]"
