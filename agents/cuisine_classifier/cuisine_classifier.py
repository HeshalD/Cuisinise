import pandas as pd
import json
from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.linear_model import Perceptron
#from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,classification_report
from imblearn.over_sampling import RandomOverSampler


train_data = pd.read_json('datasets/train.json')

train_data["ingredients_str"] = train_data["ingredients"].apply(lambda x: ' '.join(x))

vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1,3),min_df=2)
x = vectorizer.fit_transform(train_data["ingredients_str"])
y = train_data["cuisine"]

ros = RandomOverSampler(random_state=42)

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

X_res, y_res = ros.fit_resample(X_train, y_train)

#clf = Perceptron(max_iter=1000, random_state=42)
#clf = LogisticRegression(max_iter=1000, multi_class='multinomial', solver='lbfgs', class_weight='balanced', random_state=42)
clf = MLPClassifier( 
    alpha=0.0001,              # regularization term 
    hidden_layer_sizes=(150, 75),  # one hidden layer with 150 neurons and another with 75
    activation='relu',          # ReLU activation
    solver='adam',              # Adam optimizer
    max_iter=100,               # maximum epochs
    random_state=42,
    verbose=True
)

clf.fit(X_res, y_res)

y_pred = clf.predict(X_test)
print("Validation Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))