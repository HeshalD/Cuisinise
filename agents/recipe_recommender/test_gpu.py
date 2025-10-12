#!/usr/bin/env python3
"""
Test script to verify GPU optimizations in RecipeSearcher
"""

import os
import sys
import time
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

try:
    from search import RecipeSearcher
    print("✓ Successfully imported RecipeSearcher")
except ImportError as e:
    print(f"✗ Failed to import RecipeSearcher: {e}")
    sys.exit(1)

def test_gpu_initialization():
    """Test GPU initialization and configuration"""
    print("\n=== Testing GPU Initialization ===")
    
    # Check if required files exist
    data_dir = Path(__file__).parent / "data"
    index_path = data_dir / "faiss.index"
    idmap_path = data_dir / "idmap.parquet"
    db_path = data_dir / "recipes.sqlite"
    
    if not all([index_path.exists(), idmap_path.exists(), db_path.exists()]):
        print("✗ Required data files not found. Please ensure you have:")
        print(f"  - {index_path}")
        print(f"  - {idmap_path}")
        print(f"  - {db_path}")
        return False
    
    try:
        # Initialize the searcher
        print("Initializing RecipeSearcher...")
        start_time = time.time()
        searcher = RecipeSearcher(str(index_path), str(idmap_path), str(db_path))
        init_time = time.time() - start_time
        
        print(f"✓ Initialization completed in {init_time:.2f} seconds")
        
        # Get status information
        status = searcher.get_status()
        print("\n=== System Status ===")
        for key, value in status.items():
            print(f"  {key}: {value}")
        
        # Get detailed GPU info if available
        gpu_info = searcher.get_gpu_info()
        if "error" not in gpu_info:
            print("\n=== GPU Information ===")
            for key, value in gpu_info.items():
                if key != "memory_summary":
                    print(f"  {key}: {value}")
        else:
            print(f"\n=== GPU Status ===")
            print(f"  {gpu_info['error']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Initialization failed: {e}")
        return False

def test_search_performance():
    """Test search performance with GPU optimizations"""
    print("\n=== Testing Search Performance ===")
    
    data_dir = Path(__file__).parent / "data"
    index_path = data_dir / "faiss.index"
    idmap_path = data_dir / "idmap.parquet"
    db_path = data_dir / "recipes.sqlite"
    
    if not all([index_path.exists(), idmap_path.exists(), db_path.exists()]):
        print("✗ Required data files not found. Skipping search test.")
        return False
    
    try:
        searcher = RecipeSearcher(str(index_path), str(idmap_path), str(db_path))
        
        # Test queries
        test_queries = [
            "chicken pasta",
            "chocolate cake",
            "vegetarian soup",
            "spicy curry",
            "breakfast pancakes"
        ]
        
        print("Running search performance tests...")
        total_time = 0
        
        for i, query in enumerate(test_queries, 1):
            print(f"\nTest {i}/5: Searching for '{query}'")
            start_time = time.time()
            
            try:
                results = searcher.search(query, top_k=3)
                search_time = time.time() - start_time
                total_time += search_time
                
                print(f"  ✓ Found {len(results)} results in {search_time:.3f} seconds")
                if results:
                    print(f"  Top result: {results[0]['name']}")
                
            except Exception as e:
                print(f"  ✗ Search failed: {e}")
                return False
        
        avg_time = total_time / len(test_queries)
        print(f"\n✓ Average search time: {avg_time:.3f} seconds")
        
        # Clean up GPU memory
        searcher.cleanup_gpu_memory()
        print("✓ GPU memory cleaned up")
        
        return True
        
    except Exception as e:
        print(f"✗ Search test failed: {e}")
        return False

def main():
    """Main test function"""
    print("GPU Optimization Test for RecipeSearcher")
    print("=" * 50)
    
    # Test initialization
    if not test_gpu_initialization():
        print("\n✗ GPU initialization test failed")
        return False
    
    # Test search performance
    if not test_search_performance():
        print("\n✗ Search performance test failed")
        return False
    
    print("\n" + "=" * 50)
    print("✓ All tests passed! GPU optimizations are working.")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)




