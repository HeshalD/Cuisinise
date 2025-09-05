import faiss
import pandas as pd
import sqlite3
from sentence_transformers import SentenceTransformer
import spacy

# Load SpaCy if you want ingredient extraction
nlp = spacy.load("en_core_web_md")

def extract_ingredients(text):
    text = text.replace(",", " ").replace("and", " ")
    doc = nlp(text.lower())
    return [token.lemma_ for token in doc if token.pos_ in ("NOUN", "PROPN")]

def detect_dish_type(text):
    categories = ["soup", "dessert", "salad", "pasta", "cake", "stew", "curry",
                  "rice", "pizza", "sandwich", "noodles", "beverage", "breakfast",
                  "side dish", "tacos", "stir fry"]
    for cat in categories:
        if cat in text.lower():
            return cat
    return None


class RecipeSearcher:
    def __init__(self, index_path, idmap_path, db_path):
        import faiss
        import pandas as pd
        import sqlite3
        from sentence_transformers import SentenceTransformer

        self.index = faiss.read_index(index_path)
        self.idmap = pd.read_parquet(idmap_path)
        self.conn = sqlite3.connect(db_path)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def search(self, query, top_k=5):
        # Extract extra filters
        ingredients = extract_ingredients(query)  # your existing function
        dish_type = detect_dish_type(query)       # your existing function

        # Encode query
        query_vec = self.model.encode([query])

        # Search FAISS
        distances, indices = self.index.search(query_vec, top_k * 2)  # get more to allow filtering
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
