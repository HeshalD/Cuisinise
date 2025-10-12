# Simple Restaurant Finder Agent

restaurants = [
    {"name": "Pizza Place", "cuisine": "Italian", "location": "Colombo"},
    {"name": "Sushi House", "cuisine": "Japanese", "location": "Kandy"},
    {"name": "Curry Corner", "cuisine": "Sri Lankan", "location": "Colombo"},
]

def recommend(query):
    query = query.lower()
    cuisine = None
    location = None

    # Try to match cuisine and location from user query
    for r in restaurants:
        if r["cuisine"].lower() in query:
            cuisine = r["cuisine"]
        if r["location"].lower() in query:
            location = r["location"]

    # Filter results
    results = restaurants
    if cuisine:
        results = [r for r in results if r["cuisine"].lower() == cuisine.lower()]
    if location:
        results = [r for r in results if r["location"].lower() == location.lower()]
    return results

print("Welcome to Restaurant Finder Agent!")
print("Type something like to eat: ")

while True:
    user_input = input("\nYour query (type 'quit' to exit): ")
    if user_input.lower() == "quit":
        break

    matches = recommend(user_input)

    if matches:
        print("Restaurants found:")
        for r in matches:
            print(f"- {r['name']} ({r['cuisine']}) in {r['location']}")
    else:
        print("No restaurants found. Try again!")
