#!/usr/bin/env python3
"""
Performance test script for the optimized YouTube API
"""
import asyncio
import aiohttp
import time
import json
from typing import List, Dict

class PerformanceTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def test_single_search(self, query: str, top_k: int = 5) -> Dict:
        """Test a single search request"""
        start_time = time.time()
        
        payload = {
            "recipe_name": query,
            "top_k": top_k
        }
        
        async with self.session.post(
            f"{self.base_url}/search_videos",
            json=payload
        ) as response:
            result = await response.json()
            elapsed = time.time() - start_time
            
            return {
                "query": query,
                "status": response.status,
                "response_time": elapsed,
                "video_count": len(result.get("videos", [])),
                "success": response.status == 200
            }
    
    async def test_batch_search(self, queries: List[str], top_k: int = 5) -> Dict:
        """Test batch search functionality"""
        start_time = time.time()
        
        payload = [
            {"recipe_name": query, "top_k": top_k}
            for query in queries
        ]
        
        async with self.session.post(
            f"{self.base_url}/search_videos_batch",
            json=payload
        ) as response:
            result = await response.json()
            elapsed = time.time() - start_time
            
            return {
                "queries": queries,
                "status": response.status,
                "response_time": elapsed,
                "total_queries": len(queries),
                "success": response.status == 200,
                "results": result
            }
    
    async def test_cache_performance(self, query: str, iterations: int = 3) -> Dict:
        """Test cache performance by running the same query multiple times"""
        results = []
        
        for i in range(iterations):
            result = await self.test_single_search(query)
            results.append(result)
            # Small delay between requests
            await asyncio.sleep(0.1)
        
        # First request should be slower (cache miss), subsequent should be faster (cache hit)
        cache_hits = [r for r in results[1:] if r["response_time"] < results[0]["response_time"] * 0.5]
        
        return {
            "query": query,
            "iterations": iterations,
            "results": results,
            "cache_hits": len(cache_hits),
            "avg_first_request": results[0]["response_time"],
            "avg_cached_requests": sum(r["response_time"] for r in results[1:]) / (len(results) - 1),
            "cache_improvement": (results[0]["response_time"] - sum(r["response_time"] for r in results[1:]) / (len(results) - 1)) / results[0]["response_time"] * 100
        }
    
    async def test_concurrent_requests(self, queries: List[str], concurrent_limit: int = 5) -> Dict:
        """Test concurrent request handling"""
        start_time = time.time()
        
        # Create semaphore to limit concurrent requests
        semaphore = asyncio.Semaphore(concurrent_limit)
        
        async def limited_request(query):
            async with semaphore:
                return await self.test_single_search(query)
        
        # Execute all requests concurrently
        tasks = [limited_request(query) for query in queries]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        elapsed = time.time() - start_time
        
        successful = [r for r in results if not isinstance(r, Exception) and r.get("success", False)]
        failed = [r for r in results if isinstance(r, Exception) or not r.get("success", False)]
        
        return {
            "total_queries": len(queries),
            "concurrent_limit": concurrent_limit,
            "total_time": elapsed,
            "successful_requests": len(successful),
            "failed_requests": len(failed),
            "avg_response_time": sum(r.get("response_time", 0) for r in successful) / len(successful) if successful else 0,
            "requests_per_second": len(queries) / elapsed,
            "results": results
        }

async def run_performance_tests():
    """Run comprehensive performance tests"""
    test_queries = [
        "chicken curry",
        "pasta carbonara", 
        "chocolate cake",
        "beef stir fry",
        "vegetable soup"
    ]
    
    async with PerformanceTester() as tester:
        print("🚀 Starting YouTube API Performance Tests")
        print("=" * 50)
        
        # Test 1: Single search performance
        print("\n📊 Test 1: Single Search Performance")
        single_result = await tester.test_single_search("pasta recipe", 5)
        print(f"Query: {single_result['query']}")
        print(f"Response Time: {single_result['response_time']:.2f}s")
        print(f"Videos Found: {single_result['video_count']}")
        print(f"Success: {single_result['success']}")
        
        # Test 2: Cache performance
        print("\n💾 Test 2: Cache Performance")
        cache_result = await tester.test_cache_performance("chicken recipe", 3)
        print(f"Query: {cache_result['query']}")
        print(f"First Request: {cache_result['avg_first_request']:.2f}s")
        print(f"Cached Requests: {cache_result['avg_cached_requests']:.2f}s")
        print(f"Cache Improvement: {cache_result['cache_improvement']:.1f}%")
        
        # Test 3: Batch search performance
        print("\n📦 Test 3: Batch Search Performance")
        batch_result = await tester.test_batch_search(test_queries[:3], 3)
        print(f"Queries: {len(batch_result['queries'])}")
        print(f"Total Time: {batch_result['response_time']:.2f}s")
        print(f"Avg per Query: {batch_result['response_time'] / len(batch_result['queries']):.2f}s")
        print(f"Success: {batch_result['success']}")
        
        # Test 4: Concurrent requests
        print("\n⚡ Test 4: Concurrent Request Performance")
        concurrent_result = await tester.test_concurrent_requests(test_queries, 3)
        print(f"Total Queries: {concurrent_result['total_queries']}")
        print(f"Concurrent Limit: {concurrent_result['concurrent_limit']}")
        print(f"Total Time: {concurrent_result['total_time']:.2f}s")
        print(f"Requests/Second: {concurrent_result['requests_per_second']:.2f}")
        print(f"Successful: {concurrent_result['successful_requests']}")
        print(f"Failed: {concurrent_result['failed_requests']}")
        
        # Test 5: API status
        print("\n🔍 Test 5: API Status Check")
        async with tester.session.get(f"{tester.base_url}/status") as response:
            status = await response.json()
            print(f"Status: {status.get('status')}")
            print(f"GPU Available: {status.get('gpu_available')}")
            print(f"Cache Size: {status.get('cache_size')}")
            print(f"Thread Pool Active: {status.get('thread_pool_active')}")
        
        print("\n✅ Performance tests completed!")

if __name__ == "__main__":
    asyncio.run(run_performance_tests())



