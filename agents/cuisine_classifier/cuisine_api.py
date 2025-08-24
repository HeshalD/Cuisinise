from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer


nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

# Load model
model = joblib.load("cuisine_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

app = FastAPI()

class CuisineInput(BaseModel):
    text: str   

def preprocess_input(text: str):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)
    sw = set(stopwords.words('english'))
    filtered = [word for word in tokens if word.lower() not in sw]
    lemmatized = [lemmatizer.lemmatize(word,pos='v') for word in filtered]
    return " ".join(lemmatized) 

@app.post("/cuisine_check")
def predict_cuisine(data: CuisineInput):
    # Preprocess
    processed = preprocess_input(data.text)
    
    # Vectorize
    X = vectorizer.transform([processed])
    
    # Predict
    prediction = model.predict(X)
    
    return {"cuisine": prediction[0]}