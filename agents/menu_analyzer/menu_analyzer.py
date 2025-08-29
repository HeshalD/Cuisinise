import pandas as pd

# Load menu data
df = pd.read_csv("D:\\IRWA Project\\Cuisinise\\agents\\menu_analyzer\\Menu\\menu_data.csv")


def filter_menu(category=None, calories=None, protein=None, price_range=None, item_name=None):
    results = df.copy()
    
    if category:
        results = results[results["Category"].str.contains(category, case=False)]
    if calories:
        results = results[results["Calories"] <= calories]
    if protein:
        results = results[results["Protein"] >= protein]
    if price_range:
        results = results[results["Price"] <= price_range]
    if item_name:
        results = results[results["Item"].str.contains(item_name, case=False)]
    
    return results


# Interactive Q&A mode
def ask_user():
    print("=== Menu Analyzer Agent ===")
    
    category = input("Enter category (or press Enter to skip): ").strip() or None
    calories = input("Max calories? (or skip): ").strip()
    calories = int(calories) if calories else None
    
    protein = input("Min protein? (or skip): ").strip()
    protein = int(protein) if protein else None
    
    price = input("Max price range? (or skip): ").strip()
    price = int(price) if price else None
    
    item = input("Search by item name? (or skip): ").strip() or None
    
    result = filter_menu(category, calories, protein, price, item)
    print("\nFiltered Results:\n", result if not result.empty else "No matching items.")


# Very simple NLP handler (LLM could be added later)
def nlp_query(query):
    query = query.lower()
    results = df.copy()
    
    # Example rule-based NLP
    if "vegetarian" in query:
        results = results[results["Vegetarian"] == "Yes"]
    if "under" in query and "lkr" in query:
        price_limit = int("".join([c for c in query if c.isdigit()]))
        results = results[results["Price"] <= price_limit]
    
    return results


# Example usage
if __name__ == "__main__":
    mode = input("Do you want (1) Q&A filtering or (2) NLP query? ")
    
    if mode == "1":
        ask_user()
    else:
        query = input("Enter your query: ")
        result = nlp_query(query)
        print("\nNLP Query Results:\n", result if not result.empty else "No matching items.")
