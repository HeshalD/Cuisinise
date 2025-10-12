import faiss
import pandas as pd
import sqlite3
from sentence_transformers import SentenceTransformer
import spacy
import numpy as np
import typing as t
import os
import gc
try:
    import torch
    import torch.cuda
except Exception:  # torch may not be installed with CUDA; handle gracefully
    torch = None

# Global SpaCy model reference (initialized in RecipeSearcher._init_) so we can prefer GPU
nlp = None

def extract_ingredients(text: str) -> t.List[str]:
    if not text:
        return []
    text = text.replace(",", " ").replace("and", " ")
    doc = nlp(text.lower()) if nlp is not None else None
    if doc is None:
        return []
    return [token.lemma_ for token in doc if token.pos_ in ("NOUN", "PROPN")]

def detect_dish_type(text: str) -> t.Optional[str]:
    categories = ["soup", "dessert", "salad", "pasta", "cake", "stew", "curry",
                  "rice", "pizza", "sandwich", "noodles", "beverage", "breakfast",
                  "side dish", "tacos", "stir fry"]
    for cat in categories:
        if cat in text.lower():
            return cat
    return None


class RecipeSearcher:
    def __init__(self, index_path: str, idmap_path: str, db_path: str):
        # Enhanced GPU detection and configuration
        self.torch_device = self._detect_torch_device()
        self.faiss_device = self._detect_faiss_device()
        
        # Configure GPU memory management
        self._configure_gpu_memory()
        
        # Prefer GPU for SpaCy before loading the pipeline
        self._configure_spacy_gpu()

        # Load SpaCy model into global nlp
        global nlp
        nlp = self._load_spacy_model()

        # Load FAISS index and id map
        self.index_path = index_path  # Store for potential fallback
        self.index = faiss.read_index(index_path)
        self.idmap = pd.read_parquet(idmap_path)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)

        # Move FAISS index to GPU with better error handling
        self._configure_faiss_gpu()

        # Load embedding model with explicit device and memory optimization
        self.model = self._load_embedding_model()
    
    def _detect_torch_device(self) -> str:
        """Detect the best available PyTorch device"""
        if torch is None:
            return "cpu"
        
        if not torch.cuda.is_available():
            return "cpu"
        
        # Check if CUDA is properly configured
        try:
            torch.cuda.current_device()
            torch.cuda.get_device_name(0)
            return "cuda"
        except Exception:
            return "cpu"
    
    def _detect_faiss_device(self) -> str:
        """Detect FAISS GPU availability"""
        try:
            if hasattr(faiss, "get_num_gpus") and faiss.get_num_gpus() > 0:
                return "gpu"
        except Exception:
            pass
        return "cpu"
    
    def _configure_gpu_memory(self):
        """Configure GPU memory management"""
        if self.torch_device == "cuda" and torch is not None:
            try:
                # Set memory growth to avoid allocating all GPU memory at once
                torch.cuda.empty_cache()
                # Enable memory efficient attention if available
                os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:128"
            except Exception:
                pass
    
    def _configure_spacy_gpu(self):
        """Configure SpaCy for GPU usage"""
        if self.torch_device == "cuda":
            try:
                spacy.prefer_gpu()
                # Set GPU memory fraction for SpaCy
                os.environ["SPACY_GPU_MEMORY_FRACTION"] = "0.8"
            except Exception:
                pass
    
    def _load_spacy_model(self):
        """Load SpaCy model with GPU optimization"""
        try:
            # Try medium model first (better accuracy)
            nlp = spacy.load("en_core_web_md")
            if self.torch_device == "cuda":
                # Move model to GPU if available
                try:
                    nlp.to_gpu()
                except Exception:
                    pass
            return nlp
        except Exception:
            try:
                # Fallback to small model
                nlp = spacy.load("en_core_web_sm")
                if self.torch_device == "cuda":
                    try:
                        nlp.to_gpu()
                    except Exception:
                        pass
                return nlp
            except Exception:
                return None
    
    def _configure_faiss_gpu(self):
        """Configure FAISS for GPU usage with better error handling"""
        if self.faiss_device == "gpu":
            try:
                # Clear GPU cache before moving index
                if torch is not None and torch.cuda.is_available():
                    torch.cuda.empty_cache()
                
                # Move index to GPU with memory management
                self.index = faiss.index_cpu_to_all_gpus(self.index)
                
                # Set GPU memory options
                if hasattr(faiss, "StandardGpuResources"):
                    res = faiss.StandardGpuResources()
                    res.setTempMemory(1024 * 1024 * 1024)  # 1GB temp memory
                
            except Exception as e:
                print(f"FAISS GPU configuration failed: {e}")
                self.faiss_device = "cpu"
    
    def _load_embedding_model(self):
        """Load embedding model with GPU optimization"""
        try:
            # Load model with explicit device
            model = SentenceTransformer("all-MiniLM-L6-v2", device=self.torch_device)
            
            # Optimize for GPU if available
            if self.torch_device == "cuda":
                try:
                    # Enable mixed precision for better GPU performance
                    model.half()
                except Exception:
                    pass
                    
            return model
        except Exception:
            # Fallback to CPU
            self.torch_device = "cpu"
            return SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

    def get_status(self) -> dict:
        """Get comprehensive status including GPU memory info"""
        status = {
            "torch_device": self.torch_device,
            "faiss_device": self.faiss_device,
            "spacy_loaded": nlp is not None,
        }
        
        # Add GPU memory information if available
        if self.torch_device == "cuda" and torch is not None:
            try:
                status.update({
                    "gpu_memory_allocated": f"{torch.cuda.memory_allocated() / 1024**3:.2f} GB",
                    "gpu_memory_reserved": f"{torch.cuda.memory_reserved() / 1024**3:.2f} GB",
                    "gpu_memory_max_allocated": f"{torch.cuda.max_memory_allocated() / 1024**3:.2f} GB",
                    "gpu_device_name": torch.cuda.get_device_name(0),
                    "gpu_device_count": torch.cuda.device_count()
                })
            except Exception:
                pass
        
        return status
    
    def cleanup_gpu_memory(self):
        """Clean up GPU memory and run garbage collection"""
        if self.torch_device == "cuda" and torch is not None:
            try:
                torch.cuda.empty_cache()
                gc.collect()
            except Exception:
                pass
    
    def get_gpu_info(self) -> dict:
        """Get detailed GPU information"""
        if self.torch_device == "cuda" and torch is not None:
            try:
                return {
                    "device_name": torch.cuda.get_device_name(0),
                    "device_count": torch.cuda.device_count(),
                    "current_device": torch.cuda.current_device(),
                    "memory_allocated": torch.cuda.memory_allocated(),
                    "memory_reserved": torch.cuda.memory_reserved(),
                    "max_memory_allocated": torch.cuda.max_memory_allocated(),
                    "memory_summary": torch.cuda.memory_summary()
                }
            except Exception:
                return {"error": "Could not retrieve GPU info"}
        return {"error": "GPU not available"}

    def search(self, query: str, top_k: int = 5):
        # Extract extra filters
        ingredients = extract_ingredients(query)
        dish_type = detect_dish_type(query)

        # Encode query on the configured device with GPU optimization
        try:
            # Use GPU-optimized encoding if available
            if self.torch_device == "cuda":
                # Clear cache before encoding
                torch.cuda.empty_cache()
                
            query_vec = self.model.encode([query], convert_to_numpy=True, normalize_embeddings=False)
            if not isinstance(query_vec, np.ndarray):
                query_vec = np.array(query_vec)
            query_vec = query_vec.astype("float32", copy=False)
            
            # Move to GPU if using CUDA
            if self.torch_device == "cuda" and torch is not None:
                query_vec = torch.from_numpy(query_vec).cuda().cpu().numpy()
                
        except Exception as e:
            print(f"Encoding failed, falling back to CPU: {e}")
            # Fallback to CPU encoding
            self.torch_device = "cpu"
            query_vec = self.model.encode([query], convert_to_numpy=True, normalize_embeddings=False)
            if not isinstance(query_vec, np.ndarray):
                query_vec = np.array(query_vec)
            query_vec = query_vec.astype("float32", copy=False)

        # Search FAISS (request more results to allow post-filtering)
        try:
            distances, indices = self.index.search(query_vec, top_k * 2)
        except Exception as e:
            print(f"FAISS search failed: {e}")
            # Fallback to CPU search if GPU search fails
            if self.faiss_device == "gpu":
                self.faiss_device = "cpu"
                # Recreate index on CPU
                self.index = faiss.read_index(self.index_path)
                distances, indices = self.index.search(query_vec, top_k * 2)
        
        results = []

        for idx, score in zip(indices[0], distances[0]):
            if idx == -1:
                continue

            recipe_id = self.idmap.iloc[idx]["recipe_id"]
            recipe = self.conn.execute(
                """
                SELECT id, name, description, ingredients, steps, tags, serving_size, servings, search_terms
                FROM recipes
                WHERE id=?
                """,
                (recipe_id,)
            ).fetchone()

            if recipe:
                # Convert columns to safe strings
                recipe_safe = [(col or "") if isinstance(col, str) else col for col in recipe]

                # Optional: filter by detected dish type (checks steps as example)
                if dish_type and dish_type not in recipe_safe[4].lower():
                    continue

                # Optional: check extracted ingredients match
                if ingredients:
                    recipe_ing_list = recipe_safe[3].lower()  # ingredients column
                    if not any(ing.lower() in recipe_ing_list for ing in ingredients):
                        continue

                results.append({
                    "id": recipe_safe[0],
                    "name": recipe_safe[1],
                    "description": recipe_safe[2],
                    "ingredients": recipe_safe[3],
                    "steps": recipe_safe[4],
                    "tags": recipe_safe[5],
                    "serving_size": recipe_safe[6],
                    "servings": recipe_safe[7],
                    "search_terms": recipe_safe[8],
                    "score": float(score)
                })

            if len(results) >= top_k:
                break

        return results