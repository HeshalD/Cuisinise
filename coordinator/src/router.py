# agents/coordinator/router.py
import re
from typing import Optional
from .models import Plan

CUISINES = {
    "italian","chinese","indian","thai","japanese","mexican",
    "french","korean","greek","vietnamese","spanish","british",
    "sri lankan","sri_lankan","sri-lankan","seafood","american","moroccan"
}

PRICE_WORDS = {
    "cheap": "low", "budget": "low", "affordable": "low", "inexpensive": "low",
    "expensive": "high", "pricey": "high", "premium": "high"
}

def extract_location(text: str) -> Optional[str]:
    # crude pattern: “in X”, “near X”, “at X”, “around X”
    m = re.search(r"\b(in|near|at|around)\s+([A-Za-z0-9 .'-]+)", text, re.IGNORECASE)
    return m.group(2).strip() if m else None

def extract_price(text: str) -> Optional[str]:
    t = text.lower()
    for k, v in PRICE_WORDS.items():
        if k in t:
            return v
    return None

def extract_cuisine(text: str) -> Optional[str]:
    t = text.lower()
    for c in sorted(CUISINES, key=len, reverse=True):
        if c in t:
            return "sri_lankan" if "sri" in c else c
    return None

def detect_intents(text: str) -> list[str]:
    t = text.lower()
    intents = []

    # restaurant / location based
    if any(w in t for w in ["restaurant", "place to eat", "where to eat", "nearby"]):
        intents.append("find_restaurant")

    # recipe related
    if any(w in t for w in ["recipe", "cook", "how to make", "dish idea"]):
        intents.append("recommend_recipe")

    # nutrition / menu analysis
    if any(w in t for w in ["menu", "nutrition", "calories", "analyze"]):
        intents.append("analyze_menu")

    # fallback — if no clear intent, try cuisine classification
    if not intents:
        intents.append("classify_cuisine")

    # de-duplicate while preserving order
    seen, uniq = set(), []
    for i in intents:
        if i not in seen:
            uniq.append(i)
            seen.add(i)
    return uniq

def plan_from_query(query: str, default_location: Optional[str], top_k: int) -> Plan:
    cuisine = extract_cuisine(query)  # may be None
    location = extract_location(query) or default_location
    price = extract_price(query)
    intents = detect_intents(query)

    return Plan(
        intents=intents,
        cuisine=cuisine,
        location=location,
        price=price,
        min_rating=4.0,
        top_k=top_k
    )
