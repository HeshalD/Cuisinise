# agents/coordinator/service_clients.py
import os
import asyncio
from typing import Any, Dict, Optional
import httpx
from dotenv import load_dotenv

load_dotenv()

CUISINE_BASE = os.getenv("CUISINE_BASE_URL", "http://127.0.0.1:8001")
RESTAURANT_BASE = os.getenv("RESTAURANT_BASE_URL", "http://127.0.0.1:8003")
MENU_BASE = os.getenv("MENU_BASE_URL", "http://127.0.0.1:8002")
RECIPE_BASE = os.getenv("RECIPE_BASE_URL", "http://127.0.0.1:8004")
SPELL_BASE = os.getenv("SPELL_BASE_URL", "http://127.0.0.1:8005")
YOUTUBE_BASE = os.getenv("YOUTUBE_BASE_URL", "http://127.0.0.1:8006")
TOKEN = os.getenv("INTERNAL_TOKEN", "")

print(f"[DEBUG] Service URLs configured:")
print(f"[DEBUG] CUISINE_BASE: {CUISINE_BASE}")
print(f"[DEBUG] RESTAURANT_BASE: {RESTAURANT_BASE}")
print(f"[DEBUG] MENU_BASE: {MENU_BASE}")
print(f"[DEBUG] RECIPE_BASE: {RECIPE_BASE}")
print(f"[DEBUG] SPELL_BASE: {SPELL_BASE}")
print(f"[DEBUG] YOUTUBE_BASE: {YOUTUBE_BASE}")

HEADERS = {"X-Internal-Token": TOKEN} if TOKEN else {}

timeout = httpx.Timeout(10.0, read=20.0, write=10.0, connect=5.0)

async def call_cuisine_predict(text: str) -> Optional[str]:
    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.post(f"{CUISINE_BASE}/predict", json={"text": text}, headers=HEADERS)
        r.raise_for_status()
        return r.json().get("cuisine")

async def call_restaurant_search(cuisine: Optional[str], location: Optional[str], price: Optional[str], min_rating: float, top_k: int, query: Optional[str] = None) -> Dict[str, Any]:
    payload = {
        "query": query,
        "cuisine": cuisine,
        "location": location,
        "price": price,
        "min_rating": min_rating,
        "top_k": top_k,
    }
    print(f"[DEBUG] Calling restaurant service at: {RESTAURANT_BASE}/search")
    print(f"[DEBUG] Payload: {payload}")
    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.post(f"{RESTAURANT_BASE}/search", json=payload, headers=HEADERS)
        body_text = r.text
        print(f"[DEBUG] Restaurant response status: {r.status_code}")
        print(f"[DEBUG] Restaurant response body: {body_text[:200]}...")
        r.raise_for_status()
        return r.json()

async def call_menu_analyze(text: str) -> Dict[str, Any]:
    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.post(f"{MENU_BASE}/analyze", json={"text": text}, headers=HEADERS)
        r.raise_for_status()
        return r.json()

async def call_recipe_recommend(query: str, top_k: int) -> Dict[str, Any]:
    payload = {"query": query, "top_k": top_k}
    print(f"[DEBUG] Calling recipe service at: {RECIPE_BASE}/recommend")
    print(f"[DEBUG] Payload: {payload}")
    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.post(f"{RECIPE_BASE}/recommend", json=payload, headers=HEADERS)
        body_text = r.text
        print(f"[DEBUG] Response status: {r.status_code}")
        print(f"[DEBUG] Response body: {body_text[:200]}...")
        if r.status_code >= 400:
            raise Exception(f"Recipe service error {r.status_code}: {body_text}")
        return r.json()

async def call_youtube_search(recipe_name: str, top_k: int) -> Dict[str, Any]:
    payload = {"recipe_name": recipe_name, "top_k": top_k}
    print(f"[DEBUG] Calling YouTube service at: {YOUTUBE_BASE}/search_videos")
    print(f"[DEBUG] Payload: {payload}")
    # YouTube searches can be slower; give a more generous timeout
    yt_timeout = httpx.Timeout(20.0, read=90.0, write=20.0, connect=15.0)
    attempts = 3
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            async with httpx.AsyncClient(timeout=yt_timeout) as client:
                r = await client.post(f"{YOUTUBE_BASE}/search_videos", json=payload, headers=HEADERS)
                body_text = r.text
                print(f"[DEBUG] YouTube response status: {r.status_code}")
                print(f"[DEBUG] YouTube response body: {body_text[:200]}...")
                if r.status_code >= 400:
                    raise Exception(f"YouTube service error {r.status_code}: {body_text}")
                # Decode JSON with helpful error message
                try:
                    data = r.json()
                except Exception as json_err:
                    snippet = body_text[:200] if body_text else "<empty body>"
                    raise Exception(f"YouTube JSON parse error: {type(json_err).__name__}: {json_err}. Body snippet: {snippet}")
                # Basic schema validation
                if not isinstance(data, dict) or "videos" not in data or not isinstance(data.get("videos"), list):
                    raise Exception(f"YouTube response missing 'videos' list. Body snippet: {body_text[:200]}...")
                return data
        except (httpx.ReadTimeout, httpx.ConnectTimeout) as e:
            last_error = e
            if attempt < attempts:
                backoff_seconds = 1.5 ** attempt
                print(f"[WARN] YouTube request timeout (attempt {attempt}/{attempts}). Retrying in {backoff_seconds:.1f}s...")
                await asyncio.sleep(backoff_seconds)
                continue
            raise Exception(f"ReadTimeout after {attempts} attempts: {e}")
        except Exception as e:
            # Non-timeout errors: do not retry, just bubble up
            raise

async def call_spell_check(text: str, user_id: str | None = None, top_k: int = 3) -> Dict[str, Any]:
    payload = {"text": text, "top_k": top_k, "user_id": user_id}
    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.post(f"{SPELL_BASE}/check", json=payload, headers=HEADERS)
        r.raise_for_status()
        return r.json()

async def send_spell_feedback(original: str, suggested: str, accepted: bool, user_id: str | None = None) -> None:
    payload = {"original": original, "suggested": suggested, "accepted": accepted, "user_id": user_id}
    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.post(f"{SPELL_BASE}/feedback", json=payload, headers=HEADERS)
        r.raise_for_status()
