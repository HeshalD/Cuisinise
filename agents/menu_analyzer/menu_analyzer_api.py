from menu_analyzer import search_recipes
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    text: str
    number: int | None = None

app = FastAPI()

@app.get("/analyze")
def get_recipes(query: str, number: int | None = None):
    results = search_recipes(query, number=number or 5)
    if not results:
        # Return 200 with empty recipes for better UX with upstream callers
        return JSONResponse(content={"query": query, "recipes": []}, media_type="application/json")
    
    # Pretty format the JSON with indent
    return JSONResponse(content={"query": query, "recipes": results}, media_type="application/json")


@app.post("/analyze")
def post_recipes(payload: AnalyzeRequest):
    query = payload.text
    number = payload.number or 5
    results = search_recipes(query, number=number)
    if not results:
        return JSONResponse(content={"query": query, "recipes": []}, media_type="application/json")
    return JSONResponse(content={"query": query, "recipes": results}, media_type="application/json")



