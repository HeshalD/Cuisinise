# api.py - Restaurant Data and Business Logic
from typing import Dict, List
import re

class RestaurantAPI:
    def __init__(self):
        # Define cuisine types and their keywords
        self.cuisine_keywords = {
            'italian': ['italian', 'pizza', 'pasta', 'spaghetti', 'lasagna', 'risotto', 'marinara', 'carbonara', 'pepperoni', 'margherita'],
            'chinese': ['chinese', 'noodles', 'fried rice', 'dim sum', 'chow mein', 'kung pao', 'sweet sour', 'orange chicken', 'lo mein'],
            'indian': ['indian', 'curry', 'biryani', 'tandoori', 'masala', 'dal', 'samosa', 'naan', 'tikka', 'vindaloo', 'vegetarian'],
            'thai': ['thai', 'pad thai', 'tom yum', 'green curry', 'som tam', 'massaman', 'panang', 'thai basil'],
            'japanese': ['japanese', 'sushi', 'ramen', 'tempura', 'yakitori', 'teriyaki', 'miso', 'udon', 'sashimi', 'bento'],
            'mexican': ['mexican', 'tacos', 'burrito', 'quesadilla', 'enchilada', 'salsa', 'guacamole', 'nachos', 'fajitas'],
            'american': ['american', 'burger', 'steak', 'bbq', 'sandwich', 'fries', 'hotdog', 'wings', 'ribs'],
            'french': ['french', 'croissant', 'baguette', 'escargot', 'bouillabaisse', 'crepe', 'quiche', 'ratatouille'],
            'sri_lankan': ['sri lankan', 'kottu', 'hoppers', 'rice and curry', 'lamprais', 'string hoppers', 'pol sambol', 'fish curry', 'crab curry', 'ambul thiyal'],
            'seafood': ['seafood', 'fish', 'prawns', 'crab', 'lobster', 'shrimp', 'salmon', 'tuna', 'fresh fish', 'ocean'],
            'british': ['british', 'english', 'colonial', 'roast', 'fish and chips', 'shepherd pie', 'bangers', 'mash'],
            'international': ['international', 'fusion', 'continental', 'western', 'global', 'mixed cuisine']
        }
        
        # Location detection keywords
        self.location_indicators = ['in', 'at', 'near', 'around', 'close to', 'nearby', 'from', 'within']
        
        # Restaurant database
        self.restaurants = [
            # Colombo Restaurants
            {
                "id": 1,
                "name": "Roma Italian Restaurant",
                "cuisine": "italian",
                "location": "Colombo 3",
                "rating": 4.5,
                "address": "123 Galle Road, Colombo 3",
                "phone": "+94112345678",
                "price_range": "$",
                "description": "Authentic Italian cuisine with wood-fired pizzas and fresh pasta"
            },
            {
                "id": 2,
                "name": "Pasta Palace",
                "cuisine": "italian", 
                "location": "Colombo 7",
                "rating": 4.2,
                "address": "456 Havelock Road, Colombo 7",
                "phone": "+94112345679",
                "price_range": "$$",
                "description": "Upscale Italian dining with handmade pasta and fine wines"
            },
            {
                "id": 3,
                "name": "Spice Garden",
                "cuisine": "indian",
                "location": "Colombo 4",
                "rating": 4.3,
                "address": "789 Duplication Road, Colombo 4",
                "phone": "+94112345680",
                "price_range": "$",
                "description": "Traditional Indian curries and tandoori specialties"
            },
            {
                "id": 4,
                "name": "Dragon Palace",
                "cuisine": "chinese",
                "location": "Colombo 2",
                "rating": 4.1,
                "address": "321 York Street, Colombo 2",
                "phone": "+94112345681",
                "price_range": "$",
                "description": "Cantonese and Szechuan dishes with dim sum service"
            },
            {
                "id": 5,
                "name": "Little Italy",
                "cuisine": "italian",
                "location": "Colombo 5",
                "rating": 4.4,
                "address": "654 Wellawatte Road, Colombo 5",
                "phone": "+94112345682",
                "price_range": "$",
                "description": "Family-friendly Italian restaurant with pizza and pasta"
            },
            {
                "id": 6,
                "name": "Bangkok Street",
                "cuisine": "thai",
                "location": "Colombo 3",
                "rating": 4.2,
                "address": "789 Galle Road, Colombo 3",
                "phone": "+94112345683",
                "price_range": "$",
                "description": "Authentic Thai street food and traditional curries"
            },
            {
                "id": 7,
                "name": "Sakura Sushi",
                "cuisine": "japanese",
                "location": "Colombo 7",
                "rating": 4.6,
                "address": "321 Dharmapala Mawatha, Colombo 7",
                "phone": "+94112345684",
                "price_range": "$$",
                "description": "Fresh sushi and Japanese cuisine by experienced chefs"
            },
            {
                "id": 8,
                "name": "Curry Leaf",
                "cuisine": "sri_lankan",
                "location": "Colombo 1",
                "rating": 4.3,
                "address": "456 Main Street, Colombo 1",
                "phone": "+94112345685",
                "price_range": "$",
                "description": "Traditional Sri Lankan rice and curry with kottu roti"
            },
            {
                "id": 9,
                "name": "Ocean's Bounty",
                "cuisine": "seafood",
                "location": "Colombo 3",
                "rating": 4.4,
                "address": "987 Marine Drive, Colombo 3",
                "phone": "+94112345686",
                "price_range": "$$",
                "description": "Fresh seafood with ocean views and grilled specialties"
            },
            {
                "id": 10,
                "name": "Taco Fiesta",
                "cuisine": "mexican",
                "location": "Colombo 7",
                "rating": 4.0,
                "address": "123 Ward Place, Colombo 7",
                "phone": "+94112345687",
                "price_range": "$",
                "description": "Vibrant Mexican flavors with tacos, burritos and margaritas"
            },
            
            # Kandy Restaurants
            {
                "id": 11,
                "name": "Hill Country Restaurant",
                "cuisine": "sri_lankan",
                "location": "Kandy",
                "rating": 4.5,
                "address": "25 Temple Street, Kandy",
                "phone": "+94812345001",
                "price_range": "$",
                "description": "Traditional Sri Lankan cuisine with scenic hill country views"
            },
            {
                "id": 12,
                "name": "Kandy Garden Chinese",
                "cuisine": "chinese",
                "location": "Kandy",
                "rating": 4.1,
                "address": "78 Peradeniya Road, Kandy",
                "phone": "+94812345002",
                "price_range": "$",
                "description": "Authentic Chinese dishes in the heart of Kandy"
            },
            {
                "id": 13,
                "name": "Royal Curry House",
                "cuisine": "indian",
                "location": "Kandy",
                "rating": 4.3,
                "address": "45 Dalada Veediya, Kandy",
                "phone": "+94812345003",
                "price_range": "$",
                "description": "North and South Indian specialties near Temple of the Tooth"
            },
            
            # Galle Restaurants
            {
                "id": 14,
                "name": "Fort Printers Restaurant",
                "cuisine": "sri_lankan",
                "location": "Galle",
                "rating": 4.7,
                "address": "39 Pedlar Street, Galle Fort",
                "phone": "+94912345001",
                "price_range": "$$",
                "description": "Fine dining Sri Lankan cuisine in historic Galle Fort"
            },
            {
                "id": 15,
                "name": "Galle Face Seafood",
                "cuisine": "seafood",
                "location": "Galle",
                "rating": 4.4,
                "address": "12 Marine Drive, Galle",
                "phone": "+94912345002",
                "price_range": "$",
                "description": "Fresh catch of the day with ocean views"
            },
            {
                "id": 16,
                "name": "Mama's Galle Kitchen",
                "cuisine": "italian",
                "location": "Galle",
                "rating": 4.2,
                "address": "67 Church Street, Galle Fort",
                "phone": "+94912345003",
                "price_range": "$",
                "description": "Cozy Italian restaurant in colonial setting"
            },
            
            # Negombo Restaurants
            {
                "id": 17,
                "name": "Beach Catch Restaurant",
                "cuisine": "seafood",
                "location": "Negombo",
                "rating": 4.3,
                "address": "145 Lewis Place, Negombo",
                "phone": "+94312345001",
                "price_range": "$",
                "description": "Beachfront seafood restaurant with lagoon specialties"
            },
            {
                "id": 18,
                "name": "Negombo Spice Trail",
                "cuisine": "sri_lankan",
                "location": "Negombo",
                "rating": 4.1,
                "address": "89 Main Street, Negombo",
                "phone": "+94312345002",
                "price_range": "$",
                "description": "Local Sri Lankan flavors with fresh fish curries"
            },
            {
                "id": 19,
                "name": "Thai Garden Negombo",
                "cuisine": "thai",
                "location": "Negombo",
                "rating": 4.0,
                "address": "234 Poruthota Road, Negombo",
                "phone": "+94312345003",
                "price_range": "$",
                "description": "Authentic Thai cuisine near the airport"
            },
            
            # More locations...
            {
                "id": 20,
                "name": "Hill Club Restaurant",
                "cuisine": "british",
                "location": "Nuwara Eliya",
                "rating": 4.6,
                "address": "Grand Hotel Road, Nuwara Eliya",
                "phone": "+94522345001",
                "price_range": "$$",
                "description": "Colonial-style British cuisine in hill station atmosphere"
            }
        ]

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
        """Search and rank restaurants based on extracted entities"""
        results = []
        
        # Price range mapping
        price_low = ['$']
        price_high = ['$$', '$$$']
        
        for restaurant in self.restaurants:
            match_score = 0
            cuisine_matched = False
            location_matched = False
            
            # Cuisine matching - STRICT FILTERING
            if entities['cuisine']:
                if restaurant['cuisine'].lower() == entities['cuisine'].lower():
                    match_score += 10
                    cuisine_matched = True
                elif any(keyword in restaurant['name'].lower() for keyword in self.cuisine_keywords.get(entities['cuisine'], [])):
                    match_score += 5
                    cuisine_matched = True
                else:
                    # Skip restaurants that don't match the requested cuisine
                    continue
            else:
                # If no cuisine detected, we need at least location or some other filter
                if not entities['location']:
                    # No cuisine AND no location detected - this might be an invalid query
                    continue
                cuisine_matched = True
            
            # Location matching
            if entities['location']:
                location_query = entities['location'].lower().strip()
                
                if location_query == restaurant['location'].lower():
                    match_score += 8
                    location_matched = True
                elif location_query in restaurant['location'].lower():
                    match_score += 6
                    location_matched = True
                elif location_query in restaurant['address'].lower():
                    match_score += 4
                    location_matched = True
                elif any(loc_part in restaurant['location'].lower() for loc_part in location_query.split()):
                    match_score += 3
                    location_matched = True
                else:
                    match_score -= 5
            else:
                # No location specified, but cuisine matched
                if cuisine_matched:
                    location_matched = True
            
            # Price preference matching
            if entities.get('price_preference'):
                if entities['price_preference'] == 'low' and restaurant['price_range'] in price_low:
                    match_score += 2
                elif entities['price_preference'] == 'high' and restaurant['price_range'] in price_high:
                    match_score += 2
            
            # Rating boost
            match_score += restaurant['rating'] * 0.5
            
            # Only include if we have meaningful matches
            if match_score > 0 and (cuisine_matched or location_matched):
                # Additional check: must have either cuisine match OR location match
                if entities.get('cuisine') and not cuisine_matched:
                    continue
                if entities.get('location') and not location_matched:
                    continue
                    
                restaurant_copy = restaurant.copy()
                restaurant_copy['match_score'] = round(match_score, 1)
                results.append(restaurant_copy)
        
        # Sort results
        results.sort(key=lambda x: (x['match_score'], x['rating']), reverse=True)
        
        return results

    def get_supported_cuisines(self) -> List[str]:
        """Get list of supported cuisine types"""
        return list(self.cuisine_keywords.keys())

    def get_cuisine_keywords(self, cuisine: str) -> List[str]:
        """Get keywords for a specific cuisine"""
        return self.cuisine_keywords.get(cuisine.lower(), [])

    def get_locations(self) -> List[str]:
        """Get all unique locations"""
        locations = set()
        for restaurant in self.restaurants:
            locations.add(restaurant['location'])
        return sorted(list(locations))

    def filter_restaurants(self, cuisine=None, location=None, price_range=None, min_rating=None) -> List[Dict]:
        """Advanced filtering of restaurants"""
        filtered = self.restaurants

        if cuisine:
            filtered = [r for r in filtered if r['cuisine'].lower() == cuisine.lower()]
        
        if location:
            filtered = [r for r in filtered if location.lower() in r['location'].lower()]
        
        if price_range:
            filtered = [r for r in filtered if r['price_range'] == price_range]
        
        if min_rating:
            filtered = [r for r in filtered if r['rating'] >= min_rating]

        return filtered