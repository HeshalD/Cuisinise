# app.py - Main Flask Application
import re
from flask import Flask, request, jsonify
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
from typing import Dict, List
from flask_cors import CORS

# Import the restaurant API
from restaurant_api import RestaurantAPI

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Download required NLTK data (run once)
def setup_nltk():
    """Setup NLTK data with proper error handling"""
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("Downloading NLTK punkt...")
        nltk.download('punkt', quiet=True)

    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        print("Downloading NLTK stopwords...")
        nltk.download('stopwords', quiet=True)

    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        print("Downloading NLTK wordnet...")
        nltk.download('wordnet', quiet=True)

# Setup NLTK on import
setup_nltk()

class RestaurantNLP:
    def __init__(self, restaurant_api: RestaurantAPI):
        """Initialize NLP components"""
        self.restaurant_api = restaurant_api
        
        try:
            self.lemmatizer = WordNetLemmatizer()
            self.stop_words = set(stopwords.words('english'))
            print("NLTK components initialized successfully")
        except Exception as e:
            print(f"Warning: NLTK setup issue: {e}")
            self.lemmatizer = None
            self.stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'])

    def tokenize_query(self, query: str) -> List[str]:
        """Tokenize and preprocess the input query"""
        try:
            if self.lemmatizer:
                tokens = word_tokenize(query.lower())
            else:
                tokens = re.findall(r'\b\w+\b', query.lower())
        except Exception:
            tokens = re.findall(r'\b\w+\b', query.lower())
        
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
        
        entities['tokens'] = self.tokenize_query(query)
        
        # Analyze sentiment
        try:
            blob = TextBlob(query)
            if blob.sentiment.polarity > 0.1:
                entities['sentiment'] = 'positive'
            elif blob.sentiment.polarity < -0.1:
                entities['sentiment'] = 'negative'
        except Exception:
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
        
        for cuisine, keywords in self.restaurant_api.cuisine_keywords.items():
            matches = 0
            for keyword in keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', query_lower):
                    matches += len(keyword.split())
            
            if matches > max_matches:
                max_matches = matches
                best_cuisine = cuisine
        
        entities['cuisine'] = best_cuisine
        
        # Extract location
        for indicator in self.restaurant_api.location_indicators:
            if indicator in query_lower:
                pattern = rf"{re.escape(indicator)}\s+([a-zA-Z0-9\s]+?)(?:\s*(?:,|\.|!|\?|$|\s+(?:restaurant|food|place)))"
                match = re.search(pattern, query_lower)
                
                if match:
                    location = match.group(1).strip()
                    location_words = location.split()
                    cleaned_location = []
                    
                    for word in location_words:
                        if word not in ['the', 'a', 'an', 'and', 'or', 'but', 'some', 'any']:
                            cleaned_location.append(word)
                            if len(cleaned_location) >= 3:
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

class RestaurantFinder:
    def __init__(self):
        self.restaurant_api = RestaurantAPI()
        self.nlp_processor = RestaurantNLP(self.restaurant_api)
    
    def process_query(self, query: str) -> Dict:
        """Main method to process natural language queries and return results"""
        try:
            entities = self.nlp_processor.extract_entities(query)
            
            # Debug logging
            print(f"Processing query: '{query}'")
            print(f"Detected cuisine: {entities['cuisine']}")
            print(f"Detected location: {entities['location']}")
            print(f"Extracted tokens: {entities['tokens']}")
            
            restaurants = self.restaurant_api.search_restaurants(entities)
            
            if restaurants:
                print(f"Found {len(restaurants)} matching restaurants:")
                for r in restaurants[:3]:
                    print(f"   - {r['name']} ({r['cuisine']}) - Score: {r.get('match_score', 'N/A')}")
            else:
                print("No matching restaurants found")
            
            message = self.generate_response_message(entities, len(restaurants))
            
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
                'results': restaurants[:10],
                'total_found': len(restaurants),
                'message': message
            }
            
            return response
            
        except Exception as e:
            print(f"Error processing query: {e}")
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
                return "I couldn't understand your restaurant request. Please specify a cuisine type (like 'Italian', 'Chinese', 'Sri Lankan') or location (like 'Colombo', 'Kandy'). For example: 'I want Italian food in Colombo' or 'Chinese restaurants in Kandy'."
        
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

@app.route('/search', methods=['GET'])
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

#@app.route('/api/restaurants/list', methods=['GET'])
#def list_all_restaurants():
#    """Get all available restaurants in the database"""
#    return jsonify({
#        'success': True,
#       'restaurants': finder.restaurant_api.get_all_restaurants(),
#        'total_count': len(finder.restaurant_api.get_all_restaurants()),
#        'cuisines_available': finder.restaurant_api.get_supported_cuisines()
#    })

@app.route('/api/restaurants/<int:restaurant_id>', methods=['GET'])
def get_restaurant_by_id(restaurant_id):
    """Get specific restaurant by ID"""
    restaurant = finder.restaurant_api.get_restaurant_by_id(restaurant_id)
    if restaurant:
        return jsonify({
            'success': True,
            'restaurant': restaurant
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Restaurant not found'
        }), 404

@app.route('/api/restaurants/cuisine/<cuisine>', methods=['GET'])
def get_restaurants_by_cuisine(cuisine):
    """Get restaurants by cuisine type"""
    restaurants = finder.restaurant_api.get_restaurants_by_cuisine(cuisine)
    return jsonify({
        'success': True,
        'cuisine': cuisine,
        'restaurants': restaurants,
        'total_count': len(restaurants)
    })

@app.route('/api/restaurants/location/<location>', methods=['GET'])
def get_restaurants_by_location(location):
    """Get restaurants by location"""
    restaurants = finder.restaurant_api.get_restaurants_by_location(location)
    return jsonify({
        'success': True,
        'location': location,
        'restaurants': restaurants,
        'total_count': len(restaurants)
    })

@app.route('/api/restaurants/filter', methods=['GET'])
def filter_restaurants():
    """Filter restaurants with multiple criteria"""
    cuisine = request.args.get('cuisine')
    location = request.args.get('location')
    price_range = request.args.get('price_range')
    min_rating = request.args.get('min_rating')
    
    if min_rating:
        min_rating = float(min_rating)
    
    restaurants = finder.restaurant_api.filter_restaurants(
        cuisine=cuisine,
        location=location,
        price_range=price_range,
        min_rating=min_rating
    )
    
    return jsonify({
        'success': True,
        'filters': {
            'cuisine': cuisine,
            'location': location,
            'price_range': price_range,
            'min_rating': min_rating
        },
        'restaurants': restaurants,
        'total_count': len(restaurants)
    })

@app.route('/api/restaurants/cuisines', methods=['GET'])
def get_supported_cuisines():
    """Get all supported cuisine types"""
    return jsonify({
        'success': True,
        'supported_cuisines': finder.restaurant_api.get_supported_cuisines(),
        'total_cuisines': len(finder.restaurant_api.get_supported_cuisines())
    })

@app.route('/api/restaurants/locations', methods=['GET'])
@app.route('/api/restaurants/locations', methods=['GET'])
def get_locations():
    """Get all available locations"""
    return jsonify({
        'success': True,
        'locations': finder.restaurant_api.get_locations(),
        'total_locations': len(finder.restaurant_api.get_locations())
    })


# Run Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5000)
