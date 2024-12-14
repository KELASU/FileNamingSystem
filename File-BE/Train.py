import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

def load_data(file_path):
    return pd.read_csv(file_path)

def train_model(data):
    X = data['content']
    y = data['label']

    vectorizer = TfidfVectorizer(max_features=5000)
    X_tfidf = vectorizer.fit_transform(X)

    model = LogisticRegression()
    model.fit(X_tfidf, y)

    joblib.dump(model, 'file_naming_model.pkl')
    joblib.dump(vectorizer, 'vectorizer.pkl')
    print("Model and vectorizer saved.")
    return model, vectorizer

if __name__ == "__main__":
    data_file = input("Enter the path to the prepared data file: ")
    data = load_data(data_file)
    train_model(data)
