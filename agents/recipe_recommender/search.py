import faiss
import pandas as pd
import sqlite3
from sentence_transformers import SentenceTransformer
import spacy
import numpy as np
import typing as t
try:
    import torch
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
        # Detect devices
        self.torch_device = "cuda" if (torch is not None and hasattr(torch, "cuda") and torch.cuda.is_available()) else "cpu"
        self.faiss_device = "gpu" if hasattr(faiss, "get_num_gpus") and faiss.get_num_gpus() > 0 else "cpu"

        # Prefer GPU for SpaCy before loading the pipeline
        try:
            spacy.prefer_gpu()
        except Exception:
            pass

        # Load SpaCy model into global nlp
        global nlp
        try:
            nlp = spacy.load("en_core_web_md")
        except Exception:
            # Fallback to small model if medium model not present
            try:
                nlp = spacy.load("en_core_web_sm")
            except Exception:
                nlp = None

        # Load FAISS index and id map
        self.index = faiss.read_index(index_path)
        self.idmap = pd.read_parquet(idmap_path)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)

        # Optionally move FAISS index to GPU
        if self.faiss_device == "gpu":
            try:
                # Use all available GPUs
                self.index = faiss.index_cpu_to_all_gpus(self.index)
            except Exception:
                # If transfer fails, stay on CPU
                self.faiss_device = "cpu"

        # Load embedding model with explicit device
        try:
            self.model = SentenceTransformer("all-MiniLM-L6-v2", device=self.torch_device)
        except Exception:
            # Last resort: load on CPU
            self.torch_device = "cpu"
            self.model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

    def get_status(self) -> dict:
        return {
            "torch_device": self.torch_device,
            "faiss_device": self.faiss_device,
            "spacy_loaded": nlp is not None,
        }

    def search(self, query: str, top_k: int = 5):
        # Extract extra filters
        ingredients = extract_ingredients(query)
        dish_type = detect_dish_type(query)

        # Encode query on the configured device and ensure float32 numpy
        query_vec = self.model.encode([query], convert_to_numpy=True, normalize_embeddings=False)
        if not isinstance(query_vec, np.ndarray):
            query_vec = np.array(query_vec)
        query_vec = query_vec.astype("float32", copy=False)

        # Search FAISS (request more results to allow post-filtering)
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