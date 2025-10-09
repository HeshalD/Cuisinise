from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import yt_dlp
import json

app = FastAPI()

class RecipeQuery(BaseModel):
    recipe_name: str
    top_k: int = 5


@app.post("/search_videos")
async def search_videos(data: RecipeQuery):
    # Build a simple search query; avoid duplicating the word "recipe"
    recipe_keyword = "recipe"
    recipe_name_lower = (data.recipe_name or "").strip()
    query = recipe_name_lower if recipe_keyword in recipe_name_lower.lower() else f"{recipe_name_lower} {recipe_keyword}"
    try:
        # Respect requested top_k for youtube-dl search count (cap to a reasonable max)
        search_count = max(1, min(int(data.top_k or 5), 25))
        ydl_opts = {
            'quiet': True,
            # Fetch richer metadata so entries include proper URLs
            'extract_flat': False,
            'skip_download': True,
            'default_search': f'ytsearch{search_count}',
            'noplaylist': True,
            # Set a UA to avoid occasional blocks
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Use explicit ytsearch syntax to ensure proper search results
            result = ydl.extract_info(f"ytsearch{search_count}:{query}", download=False)

        # Print for debugging
        print("Raw yt_dlp result:")
        print(json.dumps(result, indent=2)[:1000])  # limit output to avoid spam

        entries = []
        if isinstance(result, dict) and "entries" in result:
            entries = result["entries"]
        elif isinstance(result, list):
            entries = result
        else:
            entries = [result]

        videos = []
        for entry in entries[: data.top_k or 5]:
            if not entry:
                continue
            # Prefer fully qualified URLs if available
            url = entry.get("webpage_url") or entry.get("url")
            # Some yt_dlp search results may put the literal query into url; discard non-URLs
            if url and not str(url).startswith("http"):
                url = None
            if not url:
                vid = entry.get("id")
                if vid:
                    url = f"https://www.youtube.com/watch?v={vid}"
            if not url:
                continue
            videos.append({
                "title": entry.get("title", "Untitled"),
                "url": url
            })

        if not videos:
            raise HTTPException(status_code=404, detail="No videos found")

        return {"videos": videos}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/status")
def status():
    return {"status": "ok"}
