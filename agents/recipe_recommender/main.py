from search import RecipeRecommender

def main():
    recommender = RecipeRecommender()
    print("🍲 Welcome to NLP Recipe Recommender!")

    user_input = input("Describe what ingredients you have: ")
    ranked_recipes = recommender.recommend_all(user_input)

    if ranked_recipes:
        print("\n✅ Recipes (most to least relevant):")
        for score, recipe in ranked_recipes:
            print(f"\n{recipe['title']} - Match Score: {score:.2f}")
            print("🧂 Ingredients:", ", ".join(recipe["ingredients"]))
            print("👨‍🍳 Instructions:", recipe["instructions"])
    else:
        print("\n❌ No recipes matched your ingredients!")

if __name__ == "__main__":
    main()
