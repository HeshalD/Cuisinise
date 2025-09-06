# agents/coordinator/service_clients.py
import os
from typing import Any, Dict, Optional
import httpx
from dotenv import load_dotenv

load_dotenv()

CUISINE_BASE = os.getenv("CUISINE_BASE_URL")
RESTAURANT_BASE = os.getenv("RESTAURANT_BASE_URL")
MENU_BASE = os.getenv("MENU_BASE_URL")
RECIPE_BASE = os.getenv("RECIPE_BASE_URL")
TOKEN = os.getenv("INTERNAL_TOKEN", "")

HEADERS = {"X-Internal-Token": TOKEN} if TOKEN else {}

timeout = httpx.Timeout(10.0, read=20.0, write=10.0, connect=5.0)

async def call_cuisine_predict(text: str) -> Optional[str]:
    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.post(f"{CUISINE_BASE}/predict", json={"text": text}, headers=HEADERS)
        r.raise_for_status()
        return r.json().get("cuisine")

async def call_restaurant_search(cuisine: Optional[str], location: Optional[str], price: Optional[str], min_rating: float, top_k: int) -> Dict[str, Any]:
    payload = {
        "cuisine": cuisine, "location": location, "price": price,
        "min_rating": min_rating, "top_k": top_k
    }
    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.post(f"{RESTAURANT_BASE}/search", json=payload, headers=HEADERS)
        r.raise_for_status()
        return r.json()

async def call_menu_analyze(text: str) -> Dict[str, Any]:
    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.post(f"{MENU_BASE}/analyze", json={"text": text}, headers=HEADERS)
        r.raise_for_status()
        return r.json()

async def call_recipe_recommend(cuisine: Optional[str], ingredients: Optional[list[str]], top_k: int) -> Dict[str, Any]:
    payload = {"cuisine": cuisine, "ingredients": ingredients, "top_k": top_k}
    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.post(f"{RECIPE_BASE}/recommend", json=payload, headers=HEADERS)
        r.raise_for_status()
        return r.json()
