import requests
import json

def test_restaurant_api():
    """Test the restaurant finder API"""
    base_url = "http://127.0.0.1:5000"
    
    # Test queries
    test_queries = [
        "I need to eat Italian foods in Colombo",
        "Pizza near Colombo 7",
        "Chinese food in Colombo 2",
        "Best Thai restaurants",
        "I want sushi in Colombo",
        "Sri Lankan rice and curry"
    ]
    
    print("🧪 Testing Restaurant Finder API")
    print("=" * 50)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n📝 Test {i}: {query}")
        print("-" * 30)
        
        try:
            # Make POST request
            response = requests.post(
                f"{base_url}/api/restaurants/search",
                json={"query": query}
            )
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"✅ Success: {result['success']}")
                print(f"🧠 Understood:")
                print(f"   - Cuisine: {result['understood']['cuisine']}")
                print(f"   - Location: {result['understood']['location']}")
                print(f"   - Tokens: {result['understood']['tokens']}")
                print(f"   - Sentiment: {result['understood']['sentiment']}")
                
                print(f"\n🍴 Found {result['total_found']} restaurants:")
                for restaurant in result['results'][:3]:  # Show top 3
                    print(f"   📍 {restaurant['name']} ({restaurant['cuisine']})")
                    print(f"      📍 {restaurant['address']}")
                    print(f"      ⭐ Rating: {restaurant['rating']}, Score: {restaurant['match_score']}")
                
                print(f"\n💬 Message: {result['message']}")
                
            else:
                print(f"❌ Error: {response.status_code}")
                print(response.text)
                
        except Exception as e:
            print(f"❌ Connection error: {e}")
    
    # Test API documentation
    print(f"\n\n📚 API Documentation Test")
    print("-" * 30)
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            docs = response.json()
            print(f"✅ API: {docs['message']}")
            print(f"🔗 Endpoints available: {len(docs['endpoints'])}")
            print(f"🍽️  Supported cuisines: {', '.join(docs['supported_cuisines'])}")
        else:
            print(f"❌ Error getting docs: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    test_restaurant_api()