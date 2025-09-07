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
    query: str
    location: Optional[str] = None
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
    query: str
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
    # Use location from payload if provided, else extract from query
    entities = nlp_processor.extract_entities(req.query)
    if req.location:
        entities["location"] = req.location

    results = restaurant_api.search_restaurants(entities)[:req.top_k]

    if not results:
        raise HTTPException(status_code=404, detail="No matching restaurants found.")

    message = f"Found {len(results)} {entities['cuisine'] or ''} restaurants"
    
    return SearchResponse(
        success=True,
        query=req.query,
        understood=entities,
        results=results,
        total_found=len(results),
        message=message
    )

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}
