import pandas as pd
import spacy
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

# Load NLP models
try:
    nlp = spacy.load("en_core_web_sm")
    print("✅ spaCy loaded!")
except OSError:
    print("⚠️ spaCy not available - using basic NLP")
    nlp = None

try:
    sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
    print("✅ Sentence Transformer loaded!")
except Exception:
    print("⚠️ Sentence Transformer not available")
    sentence_model = None

class ExistingFileNLP:
    def __init__(self, csv_file_path):
        """Initialize with YOUR existing CSV file"""
        self.df = pd.read_csv(csv_file_path)
        print(f"📊 Loaded {len(self.df)} items from {csv_file_path}")
        print(f"📋 Columns: {list(self.df.columns)}")
        
        self.nlp = nlp
        self.sentence_model = sentence_model
        
        # Compute embeddings for semantic search
        if self.sentence_model:
            self._compute_embeddings()
        
        # NLP category mappings
        self.semantic_mappings = {
            'healthy': ['low calorie', 'diet', 'light', 'lean', 'fitness', 'nutrition'],
            'filling': ['heavy', 'substantial', 'hearty', 'satisfying', 'big'],
            'breakfast': ['morning', 'brunch', 'early', 'start day'],
            'lunch': ['midday', 'noon', 'afternoon'],
            'dinner': ['evening', 'night', 'late'],
            'sweet': ['dessert', 'sugar', 'treat', 'candy', 'chocolate'],
            'protein': ['muscle', 'gym', 'workout', 'strength', 'high protein'],
            'vegetarian': ['veggie', 'plant', 'no meat', 'vegetable']
        }

    def _compute_embeddings(self):
        """Compute embeddings for semantic search"""
        print("🧠 Computing NLP embeddings...")
        
        # Create rich descriptions of each item
        descriptions = []
        for _, row in self.df.iterrows():
            # Use available columns to create descriptions
            desc = str(row.iloc[0])  # First column (usually item name)
            
            # Add other text columns
            for col in self.df.columns:
                if self.df[col].dtype == 'object' and col != self.df.columns[0]:
                    desc += f" {str(row[col])}"
            
            # Add nutritional context if available
            if 'Calories' in self.df.columns:
                cal = row['Calories']
                if cal < 300:
                    desc += " low calorie healthy light"
                elif cal > 600:
                    desc += " high calorie heavy filling"
            
            descriptions.append(desc)
        
        self.embeddings = self.sentence_model.encode(descriptions)
        print("✅ Embeddings ready!")

    def extract_nlp_intent(self, query):
        """Extract intent using NLP"""
        query_lower = query.lower()
        
        intents = {
            'nutritional': ['calorie', 'healthy', 'diet', 'nutrition', 'protein', 'fat', 'sodium'],
            'preference': ['want', 'like', 'craving', 'mood', 'feel like', 'prefer'],
            'comparison': ['best', 'better', 'compare', 'which', 'versus', 'top'],
            'discovery': ['show', 'find', 'what', 'list', 'available', 'options']
        }
        
        scores = {}
        for intent, keywords in intents.items():
            scores[intent] = sum(1 for keyword in keywords if keyword in query_lower)
        
        return max(scores.items(), key=lambda x: x[1])[0] if max(scores.values()) > 0 else 'discovery'

    def extract_constraints(self, query):
        """Extract filtering constraints using NLP"""
        constraints = {}
        
        # Numeric constraints
        patterns = {
            'calories': r'(?:under|less than|below)\s+(\d+)\s*(?:calorie|cal)',
            'protein': r'(?:over|more than|above)\s+(\d+)\s*(?:g|gram)?\s*protein',
            'price': r'(?:under|less than|below)\s*\$?(\d+)'
        }
        
        for constraint, pattern in patterns.items():
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                constraints[constraint] = int(match.group(1))
        
        # Semantic constraints
        if any(word in query.lower() for word in ['healthy', 'diet', 'light']):
            constraints['healthy'] = True
        if any(word in query.lower() for word in ['high protein', 'protein']):
            constraints['high_protein'] = True
        if any(word in query.lower() for word in ['low fat', 'lean']):
            constraints['low_fat'] = True
        
        return constraints

    def semantic_search(self, query, top_k=10):
        """Perform semantic search using NLP"""
        if not self.sentence_model:
            # Fallback to simple text matching
            return self._text_search(query, top_k)
        
        # Encode query
        query_embedding = self.sentence_model.encode([query])
        
        # Calculate similarities
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        
        # Get top matches
        top_indices = np.argsort(similarities)[::-1][:top_k]
        results = self.df.iloc[top_indices].copy()
        results['similarity'] = similarities[top_indices]
        
        return results

    def _text_search(self, query, top_k):
        """Fallback text search"""
        query_words = query.lower().split()
        
        # Score items based on word matches
        scores = []
        for _, row in self.df.iterrows():
            score = 0
            row_text = ' '.join(str(val).lower() for val in row.values)
            for word in query_words:
                if word in row_text:
                    score += 1
            scores.append(score)
        
        # Get top results
        top_indices = np.argsort(scores)[::-1][:top_k]
        return self.df.iloc[top_indices]

    def apply_nlp_filters(self, df, constraints):
        """Apply constraints extracted by NLP"""
        filtered = df.copy()
        
        # Apply numeric constraints if columns exist
        if 'calories' in constraints and 'Calories' in df.columns:
            filtered = filtered[filtered['Calories'] <= constraints['calories']]
        
        if 'protein' in constraints and 'Protein' in df.columns:
            filtered = filtered[filtered['Protein'] >= constraints['protein']]
        
        # Apply semantic constraints
        if constraints.get('healthy') and 'Calories' in df.columns:
            filtered = filtered[filtered['Calories'] <= 350]
        
        if constraints.get('high_protein') and 'Protein' in df.columns:
            filtered = filtered[filtered['Protein'] >= 15]
        
        if constraints.get('low_fat') and 'Total Fat' in df.columns:
            filtered = filtered[filtered['Total Fat'] <= 10]
        
        return filtered

    def nlp_filter_and_display(self, query):
        """Main NLP function: filter and display results"""
        print(f"\n🧠 Processing NLP Query: '{query}'")
        print("="*60)
        
        # Step 1: Extract intent and constraints using NLP
        intent = self.extract_nlp_intent(query)
        constraints = self.extract_constraints(query)
        
        print(f"🎯 NLP Intent: {intent}")
        if constraints:
            print(f"🔍 NLP Constraints: {constraints}")
        
        # Step 2: Semantic search
        results = self.semantic_search(query, top_k=20)
        
        # Step 3: Apply NLP-extracted filters
        if constraints:
            results = self.apply_nlp_filters(results, constraints)
        
        # Step 4: Display results
        self._display_nlp_results(results, query)
        
        # Step 5: Ask if user wants to download results
        if not results.empty:
            self._offer_download(results, query)
        
        return results
    
    def _offer_download(self, df, query):
        """Offer to download search results"""
        print("\n📥 DOWNLOAD OPTIONS:")
        print("(1) 💾 Download as CSV")
        print("(2) 📊 Download as Excel") 
        print("(3) 📄 Download as JSON")
        print("(4) ⏭️ Skip download")
        
        try:
            choice = input("Choose download option (1-4): ").strip()
            
            if choice == "1":
                self._download_csv(df, query)
            elif choice == "2":
                self._download_excel(df, query)
            elif choice == "3":
                self._download_json(df, query)
            elif choice == "4":
                print("⏭️ Skipping download")
            else:
                print("❌ Invalid choice")
                
        except Exception as e:
            print(f"❌ Download error: {e}")
    
    def _download_csv(self, df, query):
        """Download results as CSV"""
        try:
            # Create filename based on query
            safe_query = re.sub(r'[<>:"/\\|?*]', '_', query)[:30]
            filename = f"nlp_results_{safe_query}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            # Remove similarity column if it exists (for cleaner export)
            export_df = df.drop(columns=['similarity'], errors='ignore')
            
            export_df.to_csv(filename, index=False)
            print(f"✅ CSV downloaded: {filename}")
            print(f"📍 Location: {os.path.abspath(filename)}")
            
        except Exception as e:
            print(f"❌ CSV download failed: {e}")
    
    def _download_excel(self, df, query):
        """Download results as Excel with formatting"""
        try:
            # Create filename
            safe_query = re.sub(r'[<>:"/\\|?*]', '_', query)[:30]
            filename = f"nlp_results_{safe_query}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
            # Remove similarity column if it exists
            export_df = df.drop(columns=['similarity'], errors='ignore')
            
            # Create Excel with metadata
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # Main results sheet
                export_df.to_excel(writer, sheet_name='NLP_Results', index=False)
                
                # Metadata sheet
                metadata = pd.DataFrame({
                    'Search_Info': ['Query', 'Timestamp', 'Total_Results', 'NLP_Engine'],
                    'Values': [query, pd.Timestamp.now(), len(df), 'Sentence-Transformers + spaCy']
                })
                metadata.to_excel(writer, sheet_name='Search_Metadata', index=False)
            
            print(f"✅ Excel downloaded: {filename}")
            print(f"📍 Location: {os.path.abspath(filename)}")
            
        except Exception as e:
            print(f"❌ Excel download failed: {e}")
            print("💡 Try CSV format instead")
    
    def _download_json(self, df, query):
        """Download results as JSON"""
        try:
            # Create filename
            safe_query = re.sub(r'[<>:"/\\|?*]', '_', query)[:30]
            filename = f"nlp_results_{safe_query}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            # Create JSON with metadata
            export_data = {
                'search_metadata': {
                    'query': query,
                    'timestamp': pd.Timestamp.now().isoformat(),
                    'total_results': len(df),
                    'nlp_engine': 'Sentence-Transformers + spaCy'
                },
                'results': df.drop(columns=['similarity'], errors='ignore').to_dict('records')
            }
            
            import json
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"✅ JSON downloaded: {filename}")
            print(f"📍 Location: {os.path.abspath(filename)}")
            
        except Exception as e:
            print(f"❌ JSON download failed: {e}")
    
    def download_full_filtered_results(self, query, max_results=100):
        """Download comprehensive results (more items than displayed)"""
        print(f"\n📥 Generating comprehensive download for: '{query}'")
        
        # Get more results for download
        intent = self.extract_nlp_intent(query)
        constraints = self.extract_constraints(query)
        results = self.semantic_search(query, top_k=max_results)
        
        if constraints:
            results = self.apply_nlp_filters(results, constraints)
        
        print(f"📊 Preparing {len(results)} items for download...")
        self._offer_download(results, f"{query}_comprehensive")
        
        return results

    def _display_nlp_results(self, df, query):
        """Display NLP search results"""
        print(f"\n🎯 NLP Results for: '{query}'")
        print("="*60)
        
        if df.empty:
            print("❌ No items match your NLP query")
            print("💡 Try rephrasing or being more specific")
            return
        
        print(f"✅ Found {len(df)} items using NLP:")
        print()
        
        # Display first few columns and key info
        display_cols = []
        
        # Always show first column (usually item name)
        display_cols.append(df.columns[0])
        
        # Add nutritional columns if they exist
        nutrition_cols = ['Calories', 'Protein', 'Total Fat', 'Sodium', 'Category']
        for col in nutrition_cols:
            if col in df.columns:
                display_cols.append(col)
        
        for i, (_, row) in enumerate(df.head(10).iterrows(), 1):
            print(f"{i:2d}. 🍽️ {row[display_cols[0]]}")
            
            # Show available nutritional info
            for col in display_cols[1:]:
                if col in df.columns:
                    print(f"     {col}: {row[col]}")
            
            # Show similarity score if available
            if 'similarity' in row:
                print(f"     🧠 NLP Match: {row['similarity']:.3f}")
            
            print()

# ====== DEFINE YOUR CSV FILE PATH HERE ======
# Update this path to match your actual file location
YOUR_CSV_FILE_PATH = ".\Menu\menu_data.csv"
# Alternative paths you can try:
# YOUR_CSV_FILE_PATH = "menu_data.csv"  # If file is in same folder
# YOUR_CSV_FILE_PATH = r"D:\IRWA Project\Cuisinise\agents\menu_analyzer\your_file_name.csv"
# =============================================

# Global NLP searcher
_nlp_searcher = None

def initialize_with_your_file(csv_path=None):
    """Initialize NLP system with your existing file"""
    global _nlp_searcher
    
    # Use predefined path if no path provided
    if csv_path is None:
        csv_path = YOUR_CSV_FILE_PATH
    
    if not os.path.exists(csv_path):
        print(f"❌ File not found: {csv_path}")
        print("💡 Please update YOUR_CSV_FILE_PATH in the code")
        return None
    
    try:
        _nlp_searcher = ExistingFileNLP(csv_path)
        return _nlp_searcher
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        return None

def ask_user():
    """NLP interface for your existing data"""
    # Initialize with predefined file path
    searcher = initialize_with_your_file()
    if not searcher:
        return
    
    print("\n🧠 === NLP POWERED SEARCH ON YOUR DATA ===")
    print(f"📊 Using: {YOUR_CSV_FILE_PATH}")
    print("Ask me anything in natural language!")
    print("Type 'download [query]' for comprehensive results")
    print("Type 'back' to return")
    print("-" * 50)
    
    while True:
        try:
            query = input("\n🗣️ What are you looking for? ").strip()
            
            if query.lower() in ['back', 'exit']:
                break
            
            if query.lower().startswith('download '):
                # Extract the actual query after 'download '
                actual_query = query[9:].strip()
                if actual_query:
                    searcher.download_full_filtered_results(actual_query)
                else:
                    print("❌ Please provide a query after 'download'")
            elif query:
                searcher.nlp_filter_and_display(query)
            
        except KeyboardInterrupt:
            break

def nlp_query(query):
    """Process single NLP query"""
    # Use predefined file path
    searcher = initialize_with_your_file()
    if not searcher:
        return pd.DataFrame()
    
    return searcher.nlp_filter_and_display(query)

def display_results(df, title):
    """Display results (compatibility function)"""
    print(f"\n{title}")
    print("="*50)
    
    if df.empty:
        print("No results found")
        return
    
    for i, (_, row) in enumerate(df.iterrows(), 1):
        print(f"{i}. {row.iloc[0]}")  # First column
        # Show any numeric columns
        for col in df.columns[1:]:
            if pd.api.types.is_numeric_dtype(df[col]):
                print(f"   {col}: {row[col]}")
        print()