import os
import joblib
from PyPDF2 import PdfReader
import docx

def extract_text(file_path):
    """
    Extract text from a file (PDF or Word).
    """
    extension = os.path.splitext(file_path)[-1].lower()
    if extension == ".pdf":
        return PdfReader(file_path).pages[0].extract_text()  # Example: First page
    elif extension == ".docx":
        return "\n".join([para.text for para in docx.Document(file_path).paragraphs])
    return ""

def rename_files(directory, model_path, vectorizer_path):
    """
    Rename files based on content predictions.
    """
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)

    for root, _, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            try:
                content = extract_text(path)
                X_tfidf = vectorizer.transform([content])
                new_name = model.predict(X_tfidf)[0]  # Predict new name
                new_path = os.path.join(root, f"{new_name}{os.path.splitext(file)[-1]}")
                os.rename(path, new_path)
                print(f"Renamed: {file} -> {new_name}")
            except Exception as e:
                print(f"Error renaming {file}: {e}")

if __name__ == "__main__":
    directory = input("Enter the directory path to rename files: ")
    rename_files(directory, 'file_naming_model.pkl', 'vectorizer.pkl')
