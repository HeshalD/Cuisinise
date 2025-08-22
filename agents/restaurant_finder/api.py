from fastapi import FastAPI, Query
from typing import Optional

app = FastAPI()

restaurants = [
    {"name": "Pizza Place", "cuisine": "Italian", "location": "Colombo"},
    {"name": "Sushi House", "cuisine": "Japanese", "location": "Kandy"},
    {"name": "Curry Corner", "cuisine": "Sri Lankan", "location": "Colombo"},
]

@app.get("/restaurants")
def get_restaurants(
    cuisine: Optional[str] = Query(None, description="Type of cuisine"),
    location: Optional[str] = Query(None, description="Location of restaurant")
):
    results = restaurants
    if cuisine:
        results = [r for r in results if r["cuisine"].lower() == cuisine.lower()]
    if location:
        results = [r for r in results if r["location"].lower() == location.lower()]
    return {"results": results}
