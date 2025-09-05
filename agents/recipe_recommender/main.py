import os
import sys
import requests
from search import RecipeSearcher

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# ------------------- Download helper -------------------
def download_file(file_path, url):
    if not os.path.exists(file_path):
        print(f"Downloading {file_path}...")
        r = requests.get(url, stream=True)
        with open(file_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"{file_path} downloaded successfully.")

# ------------------- Files + URLs ----------------------
FILES_URLS = {
    "faiss.index": "https://drive.google.com/file/d/1Ew0tW2Dpa1-Iq4jPo68WGKscrq6FISeF/view?usp=sharing",
    "recipes.sqlite": "https://drive.google.com/file/d/1yIxD1jV-IkLrEXKldJsoqJ-UDytBImkY/view?usp=sharing",
    "idmap.parquet": "https://drive.google.com/file/d/1YN2AdbLiZfD8BTENLLWduOdzY6F4dJ_m/view?usp=sharing"
}

# ------------------- Check and download -----------------
for f, url in FILES_URLS.items():
    file_path = os.path.join(DATA_DIR, f)
    download_file(file_path, url)

# ------------------- Main -----------------------------
def main():
    # Initialize FAISS + SQLite searcher
    searcher = RecipeSearcher(
        index_path=os.path.join(DATA_DIR, "faiss.index"),
        idmap_path=os.path.join(DATA_DIR, "idmap.parquet"),
        db_path=os.path.join(DATA_DIR, "recipes.sqlite")
    )

    print("🍲 Welcome to FAISS-powered Recipe Recommender!")

    user_input = input("Describe what you want to cook (or list ingredients): ")
    results = searcher.search(user_input, top_k=5)

    if results:
        print("\n✅ Recipes (most relevant first):\n")
        for i, r in enumerate(results, start=1):
            print(f"🍽  Recipe {i}: {r['name']}  (Match Score: {r['score']:.4f})")
            print("-" * 60)
            print(f"🧂 Ingredients:\n{r['ingredients']}")
            print(f"👨‍🍳 Instructions:\n{r['steps']}")
            if r.get("tags"):
                print(f"🏷 Tags: {r['tags']}")
            if r.get("serving_size"):
                print(f"🥄 Serving Size: {r['serving_size']}")
            if r.get("servings"):
                print(f"🍽 Servings: {r['servings']}")
                print("-" * 60 + "\n")
    else:
        print("\n❌ No matching recipes found!")

if __name__ == "__main__":
    main()
