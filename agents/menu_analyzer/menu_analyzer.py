# menu_analyzer.py
import requests
import re

API_KEY = "3bb569b5acmsh4bf07f352673d36p1d065ejsnc702e5183e1e"
BASE_URL = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"

def clean_html(raw_html: str) -> str:
    """Remove HTML tags from the summary"""
    return re.sub("<.*?>", "", raw_html)

def search_recipes(query: str, number: int = 5):
    url = f"{BASE_URL}/recipes/complexSearch"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }
    params = {
        "query": query,
        "number": number
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    if not data.get("results"):
        return None
    
    recipes = []
    
    for item in data["results"]:
        recipe_id = item["id"]
        
        # Get recipe details
        info_url = f"{BASE_URL}/recipes/{recipe_id}/information"
        info_response = requests.get(info_url, headers=headers).json()
        
        # Get detailed nutrition facts
        nutrition_url = f"{BASE_URL}/recipes/{recipe_id}/nutritionWidget.json"
        nutrition_response = requests.get(nutrition_url, headers=headers).json()
        
        # Build recipe dictionary
        recipes.append({
            "title": info_response.get("title"),
            "summary": clean_html(info_response.get("summary", "")),
            "image": info_response.get("image"),
            "nutrition": {
                "calories": nutrition_response.get("calories"),
                "carbs": nutrition_response.get("carbs"),
                "fat": nutrition_response.get("fat"),
                "protein": nutrition_response.get("protein")
            }
        })
    
    return recipes

