# menu_analyzer.py
import requests
import re
from typing import Any, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

API_KEY = "3bb569b5acmsh4bf07f352673d36p1d065ejsnc702e5183e1e"
BASE_URL = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
TIMEOUT_SECONDS = 15

def clean_html(raw_html: str) -> str:
    """Remove HTML tags from the summary"""
    return re.sub("<.*?>", "", raw_html)

def search_recipes(query: str, number: int = 5):
    def get_json(url: str, headers: Dict[str, str], params: Optional[Dict[str, Any]] = None, session: Optional[requests.Session] = None) -> Dict[str, Any]:
        requester = session.get if session is not None else requests.get
        response = requester(url, headers=headers, params=params, timeout=TIMEOUT_SECONDS)
        content_type = response.headers.get("content-type", "")
        if not response.ok:
            # Raise a descriptive error to help diagnose issues like 401/403/429
            snippet = response.text[:300]
            raise ValueError(f"HTTP {response.status_code} from API for {url}: {snippet}")
        try:
            return response.json()
        except Exception:
            snippet = response.text[:300]
            raise ValueError(f"Non-JSON response for {url}. Content-Type: {content_type}. Body: {snippet}")

    url = f"{BASE_URL}/recipes/complexSearch"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        "Accept": "application/json"
    }
    params = {
        "query": query,
        "number": number
    }

    session = requests.Session()
    session.headers.update(headers)

    try:
        data = get_json(url, headers, params, session=session)
    except Exception:
        # Upstream failure (e.g., invalid key, rate limit, network). Treat as no results.
        return None
    
    if not data.get("results"):
        return None
    
    recipes = []

    def build_recipe(recipe_id: int) -> Optional[Dict[str, Any]]:
        info_url = f"{BASE_URL}/recipes/{recipe_id}/information"
        nutrition_url = f"{BASE_URL}/recipes/{recipe_id}/nutritionWidget.json"
        try:
            info_response = get_json(info_url, headers, session=session)
        except Exception:
            return None
        try:
            nutrition_response = get_json(nutrition_url, headers, session=session)
        except Exception:
            nutrition_response = {}
        return {
            "title": info_response.get("title"),
            "summary": clean_html(info_response.get("summary", "")),
            "image": info_response.get("image"),
            "nutrition": {
                "calories": nutrition_response.get("calories"),
                "carbs": nutrition_response.get("carbs"),
                "fat": nutrition_response.get("fat"),
                "protein": nutrition_response.get("protein")
            }
        }

    max_workers = min(max(1, number), 8)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for item in data["results"]:
            recipe_id = item.get("id")
            if recipe_id is None:
                continue
            futures.append(executor.submit(build_recipe, recipe_id))
        for future in as_completed(futures):
            try:
                result = future.result()
                if result:
                    recipes.append(result)
            except Exception:
                # Skip any failed recipe assembly
                continue

    return recipes or None