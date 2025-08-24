import requests

# List of dishes to test
dishes = [
    "chicken fried rice with soy sauce and vegetables",
    "sushi with salmon and avocado",
    "spicy green curry with coconut milk and basil",
    "kimchi stew with tofu and pork",
    "pho with beef and rice noodles",
    "spaghetti carbonara with pancetta and parmesan",
    "beef bourguignon with red wine and mushrooms",
    "fish and chips with tartar sauce",
    "moussaka with eggplant and ground lamb",
    "paella with seafood and saffron",
    "bbq pulled pork sandwich with coleslaw",
    "jerk chicken with rice and peas",
    "gumbo with sausage and okra",
    "tacos with ground beef, cheese, and salsa",
    "beef stroganoff with sour cream and mushrooms",
    "chicken tikka masala with naan",
    "ratatouille with zucchini, eggplant, and tomato"
]

url = "http://127.0.0.1:8000/cuisine_check"

for dish in dishes:
    payload = {"text": dish}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print(f"Dish: {dish}")
        print(f"Predicted Cuisine: {response.json()['cuisine']}\n")
    else:
        print(f"Failed to get prediction for: {dish}, Status Code: {response.status_code}")
