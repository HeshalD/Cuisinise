from menu_analyzer import search_recipes
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/analyze")
def get_recipes(query: str):
    results = search_recipes(query)
    if not results:
        raise HTTPException(status_code=404, detail="No matching recipes found.")
    
    # Pretty format the JSON with indent
    return JSONResponse(content={"query": query, "recipes": results}, media_type="application/json")



