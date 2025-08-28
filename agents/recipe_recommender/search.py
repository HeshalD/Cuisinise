import json
import spacy
from textblob import TextBlob
import fuzzy

# Load SpaCy medium English model
nlp = spacy.load("en_core_web_md")

# Soundex for phonetic matching
soundex = fuzzy.Soundex(4)

# ---------------- Utility Functions ----------------
def correct_spelling(text):
    """Correct basic spelling mistakes."""
    try:
        return str(TextBlob(text).correct())
    except:
        return text

def extract_ingredients(text):
    """
    Extract ingredient-like words from user input.
    Handles commas and other separators, falls back to splitting if SpaCy finds nothing.
    """
    # Replace commas and "and" with spaces
    text = text.replace(",", " ").replace("and", " ")
    
    doc = nlp(text.lower())
    ingredients = [token.lemma_ for token in doc if token.pos_ in ("NOUN", "PROPN")]
    
    # Fallback: add single words if none found (for typos or unrecognized words)
    if not ingredients:
        ingredients = text.lower().split()
    
    return ingredients

def match_ingredient_phonetic(user_ing, recipe_ings):
    """Return True if user ingredient sounds like any recipe ingredient."""
    user_code = soundex(user_ing.lower())
    for r_ing in recipe_ings:
        if user_code == soundex(r_ing.lower()):
            return True
    return False

def detect_dish_type(text):
    """Simple keyword-based dish type detection."""
    categories = ["soup", "dessert", "salad", "pasta", "cake", "stew", "curry",
                  "rice", "pizza", "sandwich", "noodles", "beverage", "breakfast",
                  "side dish", "tacos", "stir fry"]
    for cat in categories:
        if cat in text.lower():
            return cat
    return None

# ---------------- Recipe Recommender ----------------
class RecipeRecommender:
    def __init__(self, data_path="data/recipes.json"):
        with open(data_path, "r") as f:
            self.recipes = json.load(f)

        # Lowercased ingredients for phonetic matching
        self.all_ingredients = {ing.lower() for r in self.recipes for ing in r["ingredients"]}
        self.ingredient_docs = {ing: nlp(ing) for ing in self.all_ingredients}

    def recommend_all(self, user_input, similarity_threshold=0.85):
     corrected_input = correct_spelling(user_input)
    input_ingredients = extract_ingredients(corrected_input)
    if not input_ingredients:
        return []

    dish_type = detect_dish_type(user_input)
    filtered_recipes = [r for r in self.recipes if r.get("category") == dish_type] if dish_type else self.recipes

    matched_recipes = []

    for recipe in filtered_recipes:
        recipe_ings = [ing.lower() for ing in recipe["ingredients"]]
        ingredient_matches = 0

        for user_ing in input_ingredients:
            # Step 1: Soundex phonetic match
            if match_ingredient_phonetic(user_ing, recipe_ings):
                ingredient_matches += 1
                continue

            # Step 2: Semantic similarity fallback
            user_doc = nlp(user_ing)
            if any(user_doc.similarity(self.ingredient_docs[r_ing]) > similarity_threshold for r_ing in recipe_ings):
                ingredient_matches += 1

        if ingredient_matches > 0:
            # Match score = fraction of input ingredients matched
            match_score = ingredient_matches / len(input_ingredients)
            matched_recipes.append((match_score, recipe))

    # Sort recipes from most to least relevant
    matched_recipes.sort(key=lambda x: x[0], reverse=True)
    return matched_recipes
