import json
import spacy

# Load NLP model
nlp = spacy.load("en_core_web_md")

def extract_ingredients(text):
    doc = nlp(text.lower())
    ingredients = [token.text for token in doc if token.pos_ in ("NOUN", "PROPN")]
    return ingredients


class RecipeRecommender:
    def __init__(self, data_path="data/recipes.json"):
        with open(data_path, "r") as f:
            self.recipes = json.load(f)

    def recommend(self, input_ingredients):
        scores = []
        for recipe in self.recipes:
            matches = len(set(input_ingredients) & set(recipe["ingredients"]))
            scores.append((matches, recipe))

        scores.sort(key=lambda x: x[0], reverse=True)
        best_score, best_recipe = scores[0]

        return best_recipe if best_score > 0 else None
