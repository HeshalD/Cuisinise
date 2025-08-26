from search import RecipeRecommender, extract_ingredients

def main():
    recommender = RecipeRecommender()

    print("🍲 Welcome to NLP Recipe Recommender!")
    user_input = input("Describe what ingredients you have: ")
    ingredients = extract_ingredients(user_input)

    recipe = recommender.recommend(ingredients)

    if recipe:
        print(f"\n✅ Best Match: {recipe['title']}")
        print("🧂 Ingredients:", ", ".join(recipe["ingredients"]))
        print("👨‍🍳 Instructions:", recipe["instructions"])
    else:
        print("\n❌ No matching recipe found!")

if __name__ == "__main__":
    main()
