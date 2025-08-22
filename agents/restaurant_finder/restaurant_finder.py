# Simple Restaurant Finder Agent

restaurants = [
    {"name": "Pizza Place", "cuisine": "Italian", "location": "Colombo"},
    {"name": "Sushi House", "cuisine": "Japanese", "location": "Kandy"},
    {"name": "Curry Corner", "cuisine": "Sri Lankan", "location": "Colombo"},
]

def recommend(cuisine=None, location=None):
    results = restaurants
    if cuisine:
        results = [r for r in results if r["cuisine"].lower() == cuisine.lower()]
    if location:
        results = [r for r in results if r["location"].lower() == location.lower()]
    return results

print("Welcome to Restaurant Finder Agent!")

while True:
    cuisine_input = input("Enter cuisine type (or press Enter to skip, 'quit' to exit): ")
    if cuisine_input.lower() == "quit":
        break
    location_input = input("Enter location (or press Enter to skip): ")
    matches = recommend(cuisine_input, location_input)

    if matches:
        print("Restaurants found:")
        for r in matches:
            print(f"- {r['name']} ({r['cuisine']}) in {r['location']}")
    else:
        print("No restaurants found. Try again!")
