from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import re
from textblob import TextBlob

# Mock database / API wrapper
from restaurant_api import RestaurantAPI  # your existing wrapper

app = FastAPI(title="Restaurant Finder API")

# Enable CORS for testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Pydantic models
class SearchRequest(BaseModel):
    query: Optional[str] = None
    location: Optional[str] = None
    cuisine: Optional[str] = None
    price: Optional[str] = None
    min_rating: Optional[float] = None
    top_k: Optional[int] = 5

class RestaurantResult(BaseModel):
    id: int
    name: str
    cuisine: str
    location: str
    price: str
    rating: float
    match_score: Optional[float] = None

class SearchResponse(BaseModel):
    success: bool
    query: Optional[str] = ""
    understood: Dict
    results: List[RestaurantResult]
    total_found: int
    message: str

# NLP & entity extraction
class RestaurantNLP:
    def __init__(self, restaurant_api: RestaurantAPI):
        self.restaurant_api = restaurant_api
        self.location_indicators = ["in", "near", "around", "at"]

    def extract_entities(self, query: str) -> Dict:
        entities = {"cuisine": None, "location": None, "intent": "find_restaurant", "sentiment": "neutral"}
        
        # Cuisine detection
        query_lower = query.lower()
        max_matches = 0
        best_cuisine = None
        for cuisine, keywords in self.restaurant_api.cuisine_keywords.items():
            matches = sum(1 for kw in keywords if kw in query_lower)
            if matches > max_matches:
                max_matches = matches
                best_cuisine = cuisine
        entities["cuisine"] = best_cuisine

        # Location extraction
        for indicator in self.location_indicators:
            pattern = rf"{re.escape(indicator)}\s+([a-zA-Z0-9\s]+)"
            match = re.search(pattern, query_lower)
            if match:
                entities["location"] = match.group(1).strip()
                break

        # Sentiment
        try:
            blob = TextBlob(query)
            polarity = blob.sentiment.polarity
            if polarity > 0.1:
                entities["sentiment"] = "positive"
            elif polarity < -0.1:
                entities["sentiment"] = "negative"
        except Exception:
            entities["sentiment"] = "neutral"

        return entities

# Initialize API
restaurant_api = RestaurantAPI()
nlp_processor = RestaurantNLP(restaurant_api)

# POST endpoint for search
@app.post("/search", response_model=SearchResponse)
async def search_restaurants(req: SearchRequest):
    # Build entities from structured fields and optionally augment via NLP from query
    entities: Dict = {"cuisine": req.cuisine, "location": req.location, "intent": "find_restaurant", "sentiment": "neutral"}
    if req.query:
        extracted = nlp_processor.extract_entities(req.query)
        if not entities.get("cuisine"):
            entities["cuisine"] = extracted.get("cuisine")
        if not entities.get("location"):
            entities["location"] = extracted.get("location")

    results = restaurant_api.search_restaurants(entities)

    # Apply optional filters for price and rating
    filtered: List[Dict] = []
    # Normalize requested price to known buckets
    acceptable_prices: Optional[set] = None
    if req.price:
        rp = req.price.strip().lower()
        if rp in {"$", "$$", "$$$"}:
            acceptable_prices = {rp}
        elif rp in {"low", "cheap", "budget", "inexpensive"}:
            acceptable_prices = {"$"}
        elif rp in {"medium", "moderate", "mid"}:
            acceptable_prices = {"$$"}
        elif rp in {"high", "expensive", "premium", "pricey"}:
            acceptable_prices = {"$$$"}
        else:
            acceptable_prices = None

    for r in results:
        # Price filter: only exclude when we have a requested price bucket AND the item has a known price not in that bucket
        if acceptable_prices is not None:
            r_price = (r.get("price") or "").strip().lower()
            if r_price and r_price not in acceptable_prices:
                continue

        # Rating filter: treat 0/None as unknown; only enforce when rating is positive/known
        if req.min_rating is not None:
            rating_raw = r.get("rating")
            try:
                rating_val = float(rating_raw) if rating_raw is not None else 0.0
            except (TypeError, ValueError):
                rating_val = 0.0
            if rating_val > 0 and rating_val < req.min_rating:
                continue

        filtered.append(r)

    results = filtered[: (req.top_k or 5)]

    if not results:
        raise HTTPException(status_code=404, detail="No matching restaurants found.")

    message = f"Found {len(results)} {entities['cuisine'] or ''} restaurants"
    
    return SearchResponse(
        success=True,
        query=req.query or "",
        understood=entities,
        results=results,
        total_found=len(results),
        message=message
    )

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}
