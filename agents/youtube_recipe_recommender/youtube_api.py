from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import yt_dlp
import json
import asyncio
import aiohttp
import hashlib
import time
from functools import lru_cache
from typing import Dict, List, Optional
import logging
import concurrent.futures
import threading
from concurrent.futures import ThreadPoolExecutor
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from gpu_optimizer import initialize_gpu_optimization, optimize_video_search, get_gpu_stats
except ImportError as e:
    logger.warning(f"GPU optimizer not available: {e}")
    # Create dummy functions
    def initialize_gpu_optimization():
        return False
    def optimize_video_search(videos, query):
        return videos
    def get_gpu_stats():
        return {"gpu_available": False}

app = FastAPI()

# Global session for connection pooling
session: Optional[aiohttp.ClientSession] = None

# Cache for search results (in-memory)
search_cache: Dict[str, dict] = {}
CACHE_TTL = 300  # 5 minutes

# Thread pool for CPU-intensive tasks
thread_pool: Optional[ThreadPoolExecutor] = None

# GPU detection and optimization
try:
    import torch
    import torch.nn.functional as F
    GPU_AVAILABLE = torch.cuda.is_available()
    if GPU_AVAILABLE:
        logger.info(f"GPU acceleration available: {torch.cuda.get_device_name(0)}")
    else:
        logger.info("GPU not available, using CPU optimization")
except ImportError:
    GPU_AVAILABLE = False
    logger.info("PyTorch not available, using CPU-only optimization")

class RecipeQuery(BaseModel):
    recipe_name: str
    top_k: int = 5

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    global session, thread_pool
    connector = aiohttp.TCPConnector(
        limit=100,  # Total connection pool size
        limit_per_host=30,  # Per-host connection limit
        ttl_dns_cache=300,  # DNS cache TTL
        use_dns_cache=True,
    )
    session = aiohttp.ClientSession(
        connector=connector,
        timeout=aiohttp.ClientTimeout(total=30, connect=10)
    )
    
    # Initialize thread pool for CPU-intensive tasks
    thread_pool = ThreadPoolExecutor(max_workers=4, thread_name_prefix="yt_search")
    
    # Initialize GPU optimization
    if GPU_AVAILABLE:
        gpu_init_success = initialize_gpu_optimization()
        if gpu_init_success:
            logger.info("GPU optimization initialized successfully")
        else:
            logger.warning("GPU optimization initialization failed")

@app.on_event("shutdown")
async def shutdown_event():
    global session, thread_pool
    if session:
        await session.close()
    if thread_pool:
        thread_pool.shutdown(wait=True)

def get_cache_key(query: str, top_k: int) -> str:
    """Generate cache key for search query"""
    return hashlib.md5(f"{query}_{top_k}".encode()).hexdigest()

def is_cache_valid(timestamp: float) -> bool:
    """Check if cache entry is still valid"""
    return time.time() - timestamp < CACHE_TTL

@lru_cache(maxsize=1000)
def get_optimized_ydl_opts(search_count: int) -> dict:
    """Get optimized yt-dlp options with caching"""
    return {
        'quiet': True,
        'extract_flat': True,  # Use flat extraction for faster results
        'skip_download': True,
        'default_search': f'ytsearch{search_count}',
        'noplaylist': True,
        'no_warnings': True,
        'ignoreerrors': True,  # Continue on errors
        'socket_timeout': 10,  # Reduce timeout
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        },
        # Optimize for speed
        'writethumbnail': False,
        'writeinfojson': False,
        'writesubtitles': False,
        'writeautomaticsub': False,
        'writedescription': False,
        'writeannotations': False,
    }

async def search_videos_async(query: str, top_k: int) -> dict:
    """Async wrapper for yt-dlp search with optimized threading"""
    global thread_pool
    
    # Run yt-dlp in dedicated thread pool for better performance
    def run_ydl_search():
        search_count = max(1, min(top_k, 25))
        ydl_opts = get_optimized_ydl_opts(search_count)
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(f"ytsearch{search_count}:{query}", download=False)
    
    loop = asyncio.get_running_loop()
    if thread_pool:
        return await loop.run_in_executor(thread_pool, run_ydl_search)
    else:
        # Fallback to default executor
        return await loop.run_in_executor(None, run_ydl_search)

@app.post("/search_videos")
async def search_videos(data: RecipeQuery):
    start_time = time.time()
    global search_cache
    
    # Build optimized search query
    recipe_keyword = "recipe"
    recipe_name_lower = (data.recipe_name or "").strip()
    query = recipe_name_lower if recipe_keyword in recipe_name_lower.lower() else f"{recipe_name_lower} {recipe_keyword}"
    
    # Check cache first
    cache_key = get_cache_key(query, data.top_k)
    if cache_key in search_cache:
        cached_data, timestamp = search_cache[cache_key]
        if is_cache_valid(timestamp):
            logger.info(f"Cache hit for query: {query}")
            return cached_data
    
    try:
        # Use async search
        result = await search_videos_async(query, data.top_k)
        
        # Process results efficiently
        entries = []
        if isinstance(result, dict) and "entries" in result:
            entries = result["entries"]
        elif isinstance(result, list):
            entries = result
        else:
            entries = [result] if result else []

        videos = []
        for entry in entries[:data.top_k or 5]:
            if not entry:
                continue
                
            # Extract URL efficiently
            url = entry.get("webpage_url") or entry.get("url")
            if not url or not str(url).startswith("http"):
                vid = entry.get("id")
                if vid:
                    url = f"https://www.youtube.com/watch?v={vid}"
                else:
                    continue
            
            videos.append({
                "title": entry.get("title", "Untitled"),
                "url": url,
                "duration": entry.get("duration"),
                "view_count": entry.get("view_count"),
                "uploader": entry.get("uploader")
            })
        
        # Apply GPU optimization for better ranking
        if GPU_AVAILABLE and videos:
            try:
                videos = optimize_video_search(videos, query)
                logger.info(f"Applied GPU optimization to {len(videos)} videos")
            except Exception as e:
                logger.warning(f"GPU optimization failed, using original results: {e}")

        if not videos:
            raise HTTPException(status_code=404, detail="No videos found")

        response_data = {"videos": videos}
        
        # Cache the result
        search_cache[cache_key] = (response_data, time.time())
        
        # Clean old cache entries periodically
        if len(search_cache) > 1000:
            current_time = time.time()
            search_cache = {
                k: v for k, v in search_cache.items() 
                if current_time - v[1] < CACHE_TTL
            }
        
        elapsed_time = time.time() - start_time
        logger.info(f"Search completed in {elapsed_time:.2f}s for query: {query}")
        
        return response_data

    except Exception as e:
        logger.error(f"Search error for query '{query}': {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search_videos_batch")
async def search_videos_batch(queries: List[RecipeQuery] = Body(...)):
    """Batch search for multiple queries with parallel processing"""
    start_time = time.time()
    
    # Process queries in parallel
    tasks = []
    for query_data in queries:
        task = search_videos(query_data)
        tasks.append(task)
    
    # Execute all searches concurrently
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Process results
    batch_results = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            batch_results.append({
                "query": queries[i].recipe_name,
                "error": str(result),
                "videos": []
            })
        else:
            batch_results.append({
                "query": queries[i].recipe_name,
                "videos": result.get("videos", [])
            })
    
    elapsed_time = time.time() - start_time
    logger.info(f"Batch search completed in {elapsed_time:.2f}s for {len(queries)} queries")
    
    return {
        "results": batch_results,
        "total_queries": len(queries),
        "processing_time": elapsed_time
    }

@app.get("/status")
def status():
    gpu_stats = get_gpu_stats() if GPU_AVAILABLE else {"gpu_available": False}
    
    return {
        "status": "ok",
        "gpu_available": GPU_AVAILABLE,
        "gpu_stats": gpu_stats,
        "cache_size": len(search_cache),
        "thread_pool_active": thread_pool is not None
    }

@app.get("/cache/clear")
async def clear_cache():
    """Clear the search cache"""
    global search_cache
    cache_size = len(search_cache)
    search_cache.clear()
    return {"message": f"Cleared {cache_size} cache entries"}

@app.get("/cache/stats")
def cache_stats():
    """Get cache statistics"""
    current_time = time.time()
    valid_entries = sum(1 for _, (_, timestamp) in search_cache.items() 
                       if current_time - timestamp < CACHE_TTL)
    
    return {
        "total_entries": len(search_cache),
        "valid_entries": valid_entries,
        "cache_ttl": CACHE_TTL
    }
