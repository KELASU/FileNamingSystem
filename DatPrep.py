import os
import pandas as pd
from PyPDF2 import PdfReader
import docx

def extract_text_from_pdf(file_path):
    """
    Extract text from a PDF file.
    """
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file_path):
    """
    Extract text from a Word document (.docx).
    """
    doc = docx.Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def collect_file_data(directory):
    """
    Collect metadata and text content from files in a directory.
    """
    data = []
    for root, _, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            extension = os.path.splitext(file)[-1].lower()
            content = ""
            try:
                if extension == ".pdf":
                    content = extract_text_from_pdf(path)
                elif extension == ".docx":
                    content = extract_text_from_docx(path)
                else:
                    continue  # Skip unsupported formats
                data.append({
                    "filename": file,
                    "extension": extension,
                    "size": os.path.getsize(path),
                    "created_at": os.path.getctime(path),
                    "content": content
                })
            except Exception as e:
                print(f"Error processing {file}: {e}")
    return pd.DataFrame(data)

if __name__ == "__main__":
    directory = input("Enter the directory path to process files: ")
    file_data = collect_file_data(directory)
    file_data.to_csv('prepared_data_with_content.csv', index=False)
    print("Data preparation complete. Saved to 'prepared_data_with_content.csv'.")
