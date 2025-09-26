# agents/coordinator/models.py
from typing import Optional, List, Literal, Dict, Any
from pydantic import BaseModel, Field

Intent = Literal["classify_cuisine", "find_restaurant", "analyze_menu", "recommend_recipe"]

class QueryRequest(BaseModel):
    query: str
    location: Optional[str] = Field(default=None, description="Optional location (city/area). Omit to use defaults.")
    top_k: int = Field(default=5, ge=1, le=20, description="Max results to return.")

    class Config:
        json_schema_extra = {
            "examples": [
                {"query": "Analyze nutrition for Mediterranean salad", "top_k": 3},
                {"query": "Find Italian restaurants near Colombo", "location": "Colombo", "top_k": 5}
            ]
        }

class Plan(BaseModel):
    intents: List[Intent]
    cuisine: Optional[str] = None
    location: Optional[str] = None
    price: Optional[Literal["low","medium","high"]] = None
    min_rating: Optional[float] = 4.0
    top_k: int = 5

class CoordinatorResponse(BaseModel):
    plan: Plan
    results: Dict[str, Any]
