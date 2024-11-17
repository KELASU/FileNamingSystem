import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

def load_data(file_path):
    """
    Load the prepared data with content.
    """
    return pd.read_csv(file_path)

def train_model(data):
    """
    Train a model to extract topic, student ID, and name from file content.
    """
    # Example: Split the content into fields (requires labeled data)
    # Assume 'content' contains the text and 'label' is a combination of the topic, student ID, and name.
    X = data['content']
    y = data['label']  # Example: "topic_studentid_name"

    # Convert text data to numerical form using TF-IDF
    vectorizer = TfidfVectorizer(max_features=5000)
    X_tfidf = vectorizer.fit_transform(X)

    # Train a simple classification model
    model = LogisticRegression()
    model.fit(X_tfidf, y)

    # Save the model and vectorizer
    joblib.dump(model, 'file_naming_model.pkl')
    joblib.dump(vectorizer, 'vectorizer.pkl')
    print("Model and vectorizer saved.")
    return model, vectorizer

if __name__ == "__main__":
    data_file = input("Enter the path to the prepared data file: ")
    data = load_data(data_file)
    train_model(data)
