import re
from flask import Flask, request, jsonify
import requests
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
import json
from typing import Dict, List, Tuple
from flask_cors import CORS


# Download required NLTK data (run once)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("📥 Downloading NLTK punkt...")
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    print("📥 Downloading NLTK stopwords...")
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    print("📥 Downloading NLTK wordnet...")
    nltk.download('wordnet')

app = Flask(__name__)

class RestaurantNLP:
    def __init__(self):
        """Initialize NLP components"""
        try:
            self.lemmatizer = WordNetLemmatizer()
            self.stop_words = set(stopwords.words('english'))
        except Exception as e:
            print(f"⚠️  Warning: NLTK setup issue: {e}")
            self.lemmatizer = None
            self.stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'])
        
        # Define cuisine types and their keywords
        self.cuisine_keywords = {
            'italian': ['italian', 'pizza', 'pasta', 'spaghetti', 'lasagna', 'risotto', 'marinara', 'carbonara', 'pepperoni', 'margherita'],
            'chinese': ['chinese', 'noodles', 'fried rice', 'dim sum', 'chow mein', 'kung pao', 'sweet sour', 'orange chicken', 'lo mein'],
            'indian': ['indian', 'curry', 'biryani', 'tandoori', 'masala', 'dal', 'samosa', 'naan', 'tikka', 'vindaloo'],
            'thai': ['thai', 'pad thai', 'tom yum', 'green curry', 'som tam', 'massaman', 'panang', 'thai basil'],
            'japanese': ['japanese', 'sushi', 'ramen', 'tempura', 'yakitori', 'teriyaki', 'miso', 'udon', 'sashimi', 'bento'],
            'mexican': ['mexican', 'tacos', 'burrito', 'quesadilla', 'enchilada', 'salsa', 'guacamole', 'nachos', 'fajitas'],
            'american': ['american', 'burger', 'steak', 'bbq', 'sandwich', 'fries', 'hotdog', 'wings', 'ribs'],
            'french': ['french', 'croissant', 'baguette', 'escargot', 'bouillabaisse', 'crepe', 'quiche', 'ratatouille'],
            'sri_lankan': ['sri lankan', 'kottu', 'hoppers', 'rice and curry', 'lamprais', 'string hoppers', 'pol sambol'],
            'seafood': ['seafood', 'fish', 'prawns', 'crab', 'lobster', 'shrimp', 'salmon', 'tuna']
        }
        
        # Location detection keywords
        self.location_indicators = ['in', 'at', 'near', 'around', 'close to', 'nearby', 'from', 'within']
        
        # Mock restaurant database (replace with real database in production)
        self.restaurants = [
            {
                "id": 1,
                "name": "Roma Italian Restaurant",
                "cuisine": "italian",
                "location": "Colombo 3",
                "rating": 4.5,
                "address": "123 Galle Road, Colombo 3",
                "phone": "+94112345678",
                "price_range": "$$",
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
                "price_range": "$$$",
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
                "price_range": "$$",
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
                "price_range": "$$",
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
                "price_range": "$$",
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
                "price_range": "$$",
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
                "price_range": "$$$",
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
                "price_range": "$$$",
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
                "price_range": "$$",
                "description": "Vibrant Mexican flavors with tacos, burritos and margaritas"
            }
        ]

    def tokenize_query(self, query: str) -> List[str]:
        """Tokenize and preprocess the input query"""
        try:
            # Use NLTK tokenization if available
            tokens = word_tokenize(query.lower())
        except Exception:
            # Fallback to simple split if NLTK fails
            tokens = re.findall(r'\b\w+\b', query.lower())
        
        # Remove stopwords and lemmatize
        processed_tokens = []
        for token in tokens:
            if token.isalpha() and token not in self.stop_words:
                if self.lemmatizer:
                    try:
                        lemmatized = self.lemmatizer.lemmatize(token)
                        processed_tokens.append(lemmatized)
                    except Exception:
                        processed_tokens.append(token)
                else:
                    processed_tokens.append(token)
        
        return processed_tokens

    def extract_entities(self, query: str) -> Dict:
        """Extract cuisine, location, and other entities from the query"""
        entities = {
            'cuisine': None,
            'location': None,
            'tokens': [],
            'intent': 'find_restaurant',
            'sentiment': 'neutral',
            'price_preference': None
        }
        
        # Tokenize query
        entities['tokens'] = self.tokenize_query(query)
        
        # Analyze sentiment using TextBlob
        try:
            blob = TextBlob(query)
            if blob.sentiment.polarity > 0.1:
                entities['sentiment'] = 'positive'
            elif blob.sentiment.polarity < -0.1:
                entities['sentiment'] = 'negative'
        except Exception:
            # Fallback sentiment analysis
            positive_words = ['best', 'good', 'great', 'excellent', 'amazing', 'want', 'need', 'love', 'delicious']
            negative_words = ['bad', 'terrible', 'awful', 'hate', 'worst', 'horrible']
            
            query_lower = query.lower()
            if any(word in query_lower for word in positive_words):
                entities['sentiment'] = 'positive'
            elif any(word in query_lower for word in negative_words):
                entities['sentiment'] = 'negative'
        
        # Extract cuisine type using keyword matching
        query_lower = query.lower()
        max_matches = 0
        best_cuisine = None
        
        for cuisine, keywords in self.cuisine_keywords.items():
            matches = 0
            for keyword in keywords:
                if keyword in query_lower:
                    matches += len(keyword.split())  # Multi-word phrases get higher weight
            
            if matches > max_matches:
                max_matches = matches
                best_cuisine = cuisine
        
        entities['cuisine'] = best_cuisine
        
        # Extract location using pattern matching
        for indicator in self.location_indicators:
            if indicator in query_lower:
                # Create regex pattern to find location after indicator
                pattern = rf"{re.escape(indicator)}\s+([a-zA-Z0-9\s]+?)(?:\s*(?:,|\.|!|\?|$|\s+(?:restaurant|food|place)))"
                match = re.search(pattern, query_lower)
                
                if match:
                    location = match.group(1).strip()
                    # Clean up location (remove common filler words)
                    location_words = location.split()
                    cleaned_location = []
                    
                    for word in location_words:
                        if word not in ['the', 'a', 'an', 'and', 'or', 'but', 'some', 'any']:
                            cleaned_location.append(word)
                            if len(cleaned_location) >= 3:  # Limit to 3 words max
                                break
                    
                    if cleaned_location:
                        entities['location'] = ' '.join(cleaned_location)
                        break
        
        # Extract price preference
        if any(word in query_lower for word in ['cheap', 'budget', 'affordable', 'inexpensive']):
            entities['price_preference'] = 'low'
        elif any(word in query_lower for word in ['expensive', 'upscale', 'fine dining', 'luxury']):
            entities['price_preference'] = 'high'
        
        return entities

    def search_restaurants(self, entities: Dict) -> List[Dict]:
        """Search and rank restaurants based on extracted entities"""
        results = []
        
        for restaurant in self.restaurants:
            match_score = 0
            
            # Cuisine matching (highest priority)
            if entities['cuisine']:
                if restaurant['cuisine'].lower() == entities['cuisine'].lower():
                    match_score += 10  # Exact cuisine match
                # Check if restaurant name contains cuisine-related words
                elif any(keyword in restaurant['name'].lower() for keyword in self.cuisine_keywords.get(entities['cuisine'], [])):
                    match_score += 5   # Partial cuisine match
            
            # Location matching (high priority)
            if entities['location']:
                location_query = entities['location'].lower()
                
                # Exact location match
                if location_query in restaurant['location'].lower():
                    match_score += 8
                # Address contains location
                elif location_query in restaurant['address'].lower():
                    match_score += 6
                # Partial location match (e.g., "colombo" matches "Colombo 3")
                elif any(loc_part in restaurant['location'].lower() for loc_part in location_query.split()):
                    match_score += 4
            
            # Price preference matching
            if entities['price_preference']:
                price_map = {'$': 'low', '$$': 'medium', '$$$': 'high'}
                restaurant_price = price_map.get(restaurant['price_range'], 'medium')
                
                if entities['price_preference'] == restaurant_price:
                    match_score += 2
                elif entities['price_preference'] == 'low' and restaurant_price == 'medium':
                    match_score += 1  # Acceptable alternative
            
            # Rating boost (quality factor)
            match_score += restaurant['rating'] * 0.5
            
            # If no specific filters, include all restaurants with base score
            if not entities['cuisine'] and not entities['location']:
                match_score = max(match_score, 1)
            
            # Only include restaurants with positive match scores
            if match_score > 0:
                restaurant_copy = restaurant.copy()
                restaurant_copy['match_score'] = round(match_score, 1)
                results.append(restaurant_copy)
        
        # Sort by match score (descending) and rating (descending)
        results.sort(key=lambda x: (x['match_score'], x['rating']), reverse=True)
        
        return results

class RestaurantFinder:
    def __init__(self):
        self.nlp_processor = RestaurantNLP()
    
    def process_query(self, query: str) -> Dict:
        """Main method to process natural language queries and return results"""
        try:
            # Extract entities from the query
            entities = self.nlp_processor.extract_entities(query)
            
            # Search for matching restaurants
            restaurants = self.nlp_processor.search_restaurants(entities)
            
            # Generate response message
            message = self.generate_response_message(entities, len(restaurants))
            
            # Prepare final response
            response = {
                'success': True,
                'query': query,
                'understood': {
                    'cuisine': entities['cuisine'],
                    'location': entities['location'],
                    'tokens': entities['tokens'],
                    'intent': entities['intent'],
                    'sentiment': entities['sentiment'],
                    'price_preference': entities['price_preference']
                },
                'results': restaurants[:10],  # Limit to top 10 results
                'total_found': len(restaurants),
                'message': message
            }
            
            return response
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'query': query
            }
    
    def generate_response_message(self, entities: Dict, count: int) -> str:
        """Generate a friendly response message based on search results"""
        if count == 0:
            if entities['cuisine'] and entities['location']:
                return f"Sorry, I couldn't find any {entities['cuisine']} restaurants in {entities['location']}."
            elif entities['cuisine']:
                return f"Sorry, I couldn't find any {entities['cuisine']} restaurants."
            elif entities['location']:
                return f"Sorry, I couldn't find any restaurants in {entities['location']}."
            else:
                return "Sorry, I couldn't find any restaurants matching your criteria."
        
        cuisine_text = f"{entities['cuisine']} " if entities['cuisine'] else ""
        location_text = f" in {entities['location']}" if entities['location'] else ""
        
        if count == 1:
            return f"Found 1 {cuisine_text}restaurant{location_text}:"
        else:
            return f"Found {count} {cuisine_text}restaurants{location_text}. Here are the best matches:"

# Initialize the restaurant finder
finder = RestaurantFinder()

# API Routes
@app.route('/api/restaurants/search', methods=['POST'])
def search_restaurants_post():
    """POST endpoint for restaurant search with JSON payload"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'JSON payload required'
            }), 400
        
        query = data.get('query', '').strip()
        if not query:
            return jsonify({
                'success': False,
                'error': 'Query parameter is required in JSON payload'
            }), 400
        
        result = finder.process_query(query)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500

@app.route('/api/restaurants/search', methods=['GET'])
def search_restaurants_get():
    """GET endpoint for restaurant search with URL parameters"""
    query = request.args.get('query', '').strip()
    
    if not query:
        return jsonify({
            'success': False,
            'error': 'Query parameter is required',
            'example': '/api/restaurants/search?query=Italian food in Colombo'
        }), 400
    
    result = finder.process_query(query)
    return jsonify(result)

@app.route('/api/restaurants/list', methods=['GET'])
def list_all_restaurants():
    """Get all available restaurants in the database"""
    return jsonify({
        'success': True,
        'restaurants': finder.nlp_processor.restaurants,
        'total_count': len(finder.nlp_processor.restaurants),
        'cuisines_available': list(finder.nlp_processor.cuisine_keywords.keys())
    })

@app.route('/api/restaurants/cuisines', methods=['GET'])
def get_supported_cuisines():
    """Get all supported cuisine types"""
    return jsonify({
        'success': True,
        'supported_cuisines': list(finder.nlp_processor.cuisine_keywords.keys()),
        'total_cuisines': len(finder.nlp_processor.cuisine_keywords)
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Restaurant Finder API with NLP',
        'version': '1.0.0',
        'nlp_status': 'active'
    })

@app.route('/', methods=['GET'])
def home():
    """API documentation and information"""
    return jsonify({
        'message': '🍽️ Restaurant Finder API with Natural Language Processing',
        'description': 'Find restaurants using natural language queries',
        'version': '1.0.0',
        'endpoints': {
            'POST /api/restaurants/search': {
                'description': 'Search restaurants with JSON payload',
                'payload': {'query': 'your search text'},
                'example': '{"query": "I need Italian food in Colombo"}'
            },
            'GET /api/restaurants/search': {
                'description': 'Search restaurants with URL parameter',
                'parameter': 'query',
                'example': '/api/restaurants/search?query=Italian food in Colombo'
            },
            'GET /api/restaurants/list': 'Get all available restaurants',
            'GET /api/restaurants/cuisines': 'Get supported cuisine types',
            'GET /api/health': 'API health check'
        },
        'example_queries': [
            'I need to eat Italian food in Colombo',
            'Find Chinese restaurants near Colombo 2',
            'Pizza places in Colombo',
            'Best Indian curry restaurants',
            'Thai food around Colombo 7',
            'Cheap seafood restaurants',
            'Sushi in Colombo'
        ],
        'supported_cuisines': list(finder.nlp_processor.cuisine_keywords.keys()),
        'nlp_features': [
            'Tokenization and preprocessing',
            'Cuisine type detection',
            'Location extraction',
            'Sentiment analysis', 
            'Price preference detection',
            'Intent recognition'
        ]
    })

if __name__ == '__main__':
    print("🍕 Starting Restaurant Finder API with NLP...")
    print("📦 Setting up NLP components...")
    
    # Initialize and check components
    try:
        test_result = finder.process_query("test")
        print("✅ NLP processing is working!")
    except Exception as e:
        print(f"⚠️  NLP setup warning: {e}")
    
    print("\n🚀 API Server Starting...")
    print("🌐 Server will be available at:")
    print("   • http://localhost:5000")
    print("   • http://127.0.0.1:5000")
    
    print("\n📚 Test URLs:")
    print("   • Documentation: http://127.0.0.1:5000")
    print("   • Search Example: http://127.0.0.1:5000/api/restaurants/search?query=Italian food in Colombo")
    print("   • All Restaurants: http://127.0.0.1:5000/api/restaurants/list")
    
    print("\n🧪 Example curl command:")
    print('curl -X POST http://127.0.0.1:5000/api/restaurants/search \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"query": "I need to eat Italian foods in Colombo"}\'')
    
    print("\n" + "="*60)
    
    # Start the Flask development server
    app.run(debug=True, host='0.0.0.0', port=5000)