import os
import requests
from fastapi import FastAPI, Query, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
import sqlite3

from search import RecipeSearcher

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# ------------------- Download helper -------------------
def download_file(file_path, url):
    if not os.path.exists(file_path):
        print(f"Downloading {file_path}...")
        r = requests.get(url, stream=True)
        with open(file_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"{file_path} downloaded successfully.")

# ------------------- Files + URLs ----------------------
FILES_URLS = {
    "faiss.index": "https://drive.google.com/uc?export=download&id=1Ew0tW2Dpa1-Iq4jPo68WGKscrq6FISeF",
    "recipes.sqlite": "https://drive.google.com/uc?export=download&id=1yIxD1jV-IkLrEXKldJsoqJ-UDytBImkY",
    "idmap.parquet": "https://drive.google.com/uc?export=download&id=1YN2AdbLiZfD8BTENLLWduOdzY6F4dJ_m",
}

# ------------------- Check and download ----------------
for f, url in FILES_URLS.items():
    file_path = os.path.join(DATA_DIR, f)
    download_file(file_path, url)

# ------------------- FastAPI App ------------------------
app = FastAPI(title="FAISS-powered Recipe Recommender")

# Initialize searcher once when app starts
searcher = RecipeSearcher(
    index_path=os.path.join(DATA_DIR, "faiss.index"),
    idmap_path=os.path.join(DATA_DIR, "idmap.parquet"),
    db_path=os.path.join(DATA_DIR, "recipes.sqlite")
)

class RecipeResult(BaseModel):
    id: int
    name: str
    description: str
    ingredients: str
    steps: str
    tags: str
    serving_size: str
    servings: str
    search_terms: str
    score: float


class RecipeQuery(BaseModel):
    query: str
    top_k: int = 5


@app.post("/recommend", response_model=List[RecipeResult])
async def search_recipes(data: RecipeQuery, request: Request):
    # Temporary debug logging
    try:
        body = await request.body()
        print("[recipe_recommender] Incoming /recommend body:", body.decode("utf-8", errors="ignore"))
    except Exception:
        pass
    try:
        results = searcher.search(data.query, top_k=data.top_k)
        if not results:
            raise HTTPException(status_code=404, detail="No matching recipes found.")
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/status")
def status():
    try:
        info = searcher.get_status() if hasattr(searcher, "get_status") else {}
        return {
            "ok": True,
            "devices": info,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))