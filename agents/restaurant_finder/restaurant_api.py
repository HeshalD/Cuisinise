# api.py - Restaurant Data and Business Logic
from typing import Dict, List
from restaurant_data import cuisine_keywords, location_indicators, restaurants
import requests

class RestaurantAPI:
    def __init__(self):
        self.cuisine_keywords = cuisine_keywords
        self.location_indicators = location_indicators
        self.restaurants = restaurants
        
        
    def fetch_restaurants_from_osm(self, lat: float, lon: float, radius: int = 3000):
        """Fetch nearby restaurants/cafes/fast_food places from OSM Overpass API"""
        ql = f"""
        [out:json][timeout:25];
        (
          node["amenity"~"^(restaurant|fast_food|cafe)$"](around:{radius},{lat},{lon});
          way["amenity"~"^(restaurant|fast_food|cafe)$"](around:{radius},{lat},{lon});
          relation["amenity"~"^(restaurant|fast_food|cafe)$"](around:{radius},{lat},{lon});
        );
        out center tags;
        """
        resp = requests.post(
            "https://overpass-api.de/api/interpreter",
            data={"data": ql},
            headers={"User-Agent": "Cuisinise/1.0 (heshaltempdissanayake@gmail.com)"}
        )
        resp.raise_for_status()
        data = resp.json()

        restaurants = []
        for e in data.get("elements", []):
            tags = e.get("tags", {})
            restaurants.append({
                "id": e.get("id"),
                "name": tags.get("name", "(no name)"),
                "cuisine": tags.get("cuisine", "unknown"),
                "location": tags.get("addr:city", "") or tags.get("addr:district", ""),
                "rating": None,  # OSM has no ratings
                "address": tags.get("addr:street", ""),
                "phone": tags.get("phone", ""),
                "price_range": None,  # not available in OSM
                "description": tags.get("description", ""),
                "lat": e.get("lat") or (e.get("center", {}) or {}).get("lat"),
                "lon": e.get("lon") or (e.get("center", {}) or {}).get("lon"),
            })
        return restaurants

    def geocode_location(self, location):
        try:
            url = f"https://nominatim.openstreetmap.org/search"
            params = {"q": location, "format": "json", "limit": 1}
            response = requests.get(url, params=params, headers={"User-Agent": "YourApp"})
            if response.status_code == 200:
                 data = response.json()
            if data:
                return {"lat": float(data[0]["lat"]), "lon": float(data[0]["lon"])}
        except Exception as e:
            print(f"Geocoding failed for {location}: {e}")
        return None

   

    def get_all_restaurants(self) -> List[Dict]:
        """Return all restaurants"""
        return self.restaurants

    def get_restaurant_by_id(self, restaurant_id: int) -> Dict:
        """Get specific restaurant by ID"""
        for restaurant in self.restaurants:
            if restaurant['id'] == restaurant_id:
                return restaurant
        return None

    def get_restaurants_by_cuisine(self, cuisine: str) -> List[Dict]:
        """Get restaurants by cuisine type"""
        cuisine_lower = cuisine.lower()
        return [r for r in self.restaurants if r['cuisine'].lower() == cuisine_lower]

    def get_restaurants_by_location(self, location: str) -> List[Dict]:
        """Get restaurants by location"""
        location_lower = location.lower()
        return [r for r in self.restaurants if location_lower in r['location'].lower()]

    def get_restaurants_by_price_range(self, price_range: str) -> List[Dict]:
        """Get restaurants by price range"""
        return [r for r in self.restaurants if r['price_range'] == price_range]

    def search_restaurants(self, entities: Dict) -> List[Dict]:
        """Search and rank restaurants using OSM and ensure FastAPI model compatibility."""
        results = []

        # --- STEP 1: Require a location ---
        if not entities.get("location"):
            print("❌ No location provided, OSM requires a location.")
            return []

        coords = self.geocode_location(entities["location"])
        if not coords:
            print("❌ Geocoding failed.")
            return []

        lat, lon = coords["lat"], coords["lon"]

        try:
            source_restaurants = self.fetch_restaurants_from_osm(lat, lon)
        except Exception as e:
            print(f"⚠️ OSM fetch failed: {e}")
            return []

        # --- STEP 2: Apply filtering & scoring ---
        for restaurant in source_restaurants:
            match_score = 0
            cuisine_matched = False
            location_matched = False

            # Cuisine matching
            if entities.get('cuisine'):
                if restaurant['cuisine'] and restaurant['cuisine'].lower() == entities['cuisine'].lower():
                    match_score += 10
                    cuisine_matched = True
                elif any(keyword in restaurant['name'].lower() 
                         for keyword in self.cuisine_keywords.get(entities['cuisine'], [])):
                    match_score += 5
                    cuisine_matched = True
                else:
                    continue  # skip if cuisine does not match
            else:
                cuisine_matched = True  # allow location-only searches

            # Location matching
            if entities.get('location') and restaurant.get("location"):
                location_query = entities['location'].lower().strip()
                rest_loc = restaurant['location'].lower()

                if location_query == rest_loc:
                    match_score += 8
                    location_matched = True
                elif location_query in rest_loc:
                    match_score += 6
                    location_matched = True
                elif restaurant.get("address") and location_query in restaurant['address'].lower():
                    match_score += 4
                    location_matched = True
                elif any(loc_part in rest_loc for loc_part in location_query.split()):
                    match_score += 3
                    location_matched = True
                else:
                    match_score -= 5
            else:
                location_matched = True

            if match_score > 0 and (cuisine_matched or location_matched):
                restaurant_copy = restaurant.copy()
                restaurant_copy['match_score'] = round(match_score, 1)

                # --- Ensure required fields for FastAPI Pydantic model ---
                if "price" not in restaurant_copy or restaurant_copy["price"] is None:
                    price_str_map = {
                        '$': '$',
                        '$$': '$$',
                        '$$$': '$$$'
                    }
                    restaurant_copy["price"] = price_str_map.get(restaurant_copy.get("price_range"), "")

                if "rating" not in restaurant_copy or restaurant_copy["rating"] is None:
                    restaurant_copy["rating"] = 0.0

                # Ensure strings are not None
                restaurant_copy["cuisine"] = restaurant_copy.get("cuisine") or "unknown"
                restaurant_copy["location"] = restaurant_copy.get("location") or ""
                restaurant_copy["name"] = restaurant_copy.get("name") or "(no name)"

                results.append(restaurant_copy)

        # --- STEP 3: Sort by match score ---
        results.sort(key=lambda x: x['match_score'], reverse=True)
        return results
