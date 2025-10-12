import pandas as pd
import numpy as np
import json
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.linear_model import Perceptron
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,classification_report
#from imblearn.over_sampling import RandomOverSampler
from imblearn.over_sampling import SMOTE
#from gensim.models import FastText

train_data = pd.read_json('datasets/train.json')

train_data["ingredients_str"] = train_data["ingredients"].apply(lambda x: ' '.join(x))

vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1,3),min_df=2)
x = vectorizer.fit_transform(train_data["ingredients_str"])
y = train_data["cuisine"]

#tokenized_ingredients = [ingredients.split() for ingredients in train_data["ingredients_str"]]

#fasttext_model = FastText(vector_size=50, window=3, min_count=1, workers=4)
#fasttext_model.build_vocab(sentences=tokenized_ingredients)
#fasttext_model.train(sentences=tokenized_ingredients, total_examples=len(tokenized_ingredients), epochs=10)

#def recipe_to_vec(tokens):
#    vecs = [fasttext_model.wv[word] for word in tokens if word in fasttext_model.wv]
#    return np.mean(vecs, axis=0) if vecs else np.zeros(fasttext_model.vector_size)

#X = np.array([recipe_to_vec(tokens) for tokens in tokenized_ingredients])
#y = train_data["cuisine"]

#ros = RandomOverSampler(random_state=42)
smote = SMOTE(random_state=42)

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

X_res, y_res = smote.fit_resample(X_train, y_train)

#clf = Perceptron(max_iter=1000, random_state=42)
clf = LogisticRegression(max_iter=1000, multi_class='multinomial', solver='lbfgs', class_weight='balanced', random_state=42)
#clf = MLPClassifier( 
#    alpha=0.0001,              # regularization term 
#    hidden_layer_sizes=(150, 75),  # one hidden layer with 150 neurons and another with 75
#    activation='relu',          # ReLU activation
#    solver='adam',              # Adam optimizer
#    max_iter=100,               # maximum epochs
#    random_state=42,
#    verbose=True
#)

clf.fit(X_res, y_res)

y_pred = clf.predict(X_test)
print("Validation Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

joblib.dump(clf, "cuisine_model.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")
