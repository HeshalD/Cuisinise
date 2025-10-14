# synonyms.py

# Expanded dictionary of common typos and ingredient synonyms
SYNONYMS = {
    # Chicken variations
    "chickan": "chicken",
    "chiken": "chicken",
    "chikn": "chicken",
    "chik": "chicken",

    # Rice variations
    "rice": "rice",
    "rise": "rice",
    "long grain rice": "rice",

    # Onion variations
    "onio": "onion",
    "onions": "onion",

    # Tomato variations
    "tomatoe": "tomato",
    "tomatos": "tomato",
    "tomatoes": "tomato",

    # Pepper variations
    "bell pepper": "capsicum",
    "capsicum": "capsicum",
    "red pepper": "capsicum",
    "green pepper": "capsicum",

    # Garlic variations
    "garlick": "garlic",
    "garlics": "garlic",

    # Other vegetables
    "carrot": "carrot",
    "carrots": "carrot",
    "broccoli": "broccoli",
    "cabbage": "cabbage",
    "lettuce": "lettuce",

    # Dairy
    "milk": "milk",
    "cheese": "cheese",
    "cream": "cream",
    "butter": "butter",
    "yogurt": "yogurt",

    # Protein
    "beef": "beef",
    "ground beef": "beef",
    "pork": "pork",
    "egg": "egg",
    "eggs": "egg",
    "fish": "fish",
    "chicken breast": "chicken",

    # Spices / condiments
    "soy sauce": "soy sauce",
    "sugar": "sugar",
    "salt": "salt",
    "pepper": "pepper",
    "cinnamon": "cinnamon",
    "ginger": "ginger",
    "curry powder": "curry powder",
    "chili powder": "chili powder",
}

def normalize_ingredient(ingredient):
    """Map an ingredient to its canonical form using synonyms."""
    ingredient = ingredient.lower()
    return SYNONYMS.get(ingredient, ingredient)

def normalize_ingredients_list(ingredients_list):
    """Normalize a list of ingredient strings."""
    return [normalize_ingredient(ing) for ing in ingredients_list]
