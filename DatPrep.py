import os
import pandas as pd
from PyPDF2 import PdfReader
import docx
import re
from datetime import datetime
def extract_text_from_pdf(file_path):

    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file_path):

    doc = docx.Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def extract_fields(content):

    name_id_pattern = r"(?P<name>[A-Za-z\s]+)\s*[–-]\s*(?P<student_id>\d+)"
    match = re.search(name_id_pattern, content)
    
    name = match.group("name").strip() if match else None
    student_id = match.group("student_id").strip() if match else None

    paragraphs = content.split("\n")
    topic = None
    if match:
        match_line = match.group(0)
        try:
            index = next(i for i, para in enumerate(paragraphs) if match_line in para)
            # Topic is in the next non-empty paragraph
            for para in paragraphs[index + 1:]:
                if para.strip():  # Skip empty lines
                    topic = para.strip()
                    break
        except StopIteration:
            pass

    return {
        "name": name,
        "student_id": student_id,
        "title": topic
    }

def process_folder(directory):
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
                    continue 
                
                fields = extract_fields(content)
                timestamp = os.path.getctime(path)
                readable_date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                data.append({
                    "filename": file,
                    "extension": extension,
                    "size": os.path.getsize(path),
                    "created_at": readable_date,
                    "content": content,
                    "name": fields["name"],
                    "title": fields["title"],
                    "student_id": fields["student_id"]
                })
            except Exception as e:
                print(f"Error processing {file}: {e}")
    return pd.DataFrame(data)

if __name__ == "__main__":
    directory = input("Enter the directory path containing files: ")
    processed_data = process_folder(directory)
    processed_data.to_csv('processed_data_with_fields.csv', index=False)
    print("Data preparation complete. Saved to 'processed_data_with_fields.csv'.")

