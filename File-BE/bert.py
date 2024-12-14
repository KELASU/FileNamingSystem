import os
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

# Load the pre-trained NER model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
nlp = pipeline("ner", model=model, tokenizer=tokenizer)

def extract_info_from_file(file_path):
    """Extract title, name, and ID from the content of a file."""
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Use the NER pipeline to extract entities
    ner_results = nlp(content)

    title = None
    name = None
    id_ = None

    # Process the NER results to find title, name, and ID
    for entity in ner_results:
        if entity['label'] == 'TITLE':
            title = content[entity['start']:entity['end']]
        elif entity['label'] == 'NAME':
            name = content[entity['start']:entity['end']]
        elif entity['label'] == 'ID':
            id_ = content[entity['start']:entity['end']]

    return title, name, id_

def generate_file_name(title, name, id_):
    """Generate a new file name based on the extracted information."""
    return f"{title}_{name}_{id_}.txt"

def process_files_in_directory(directory):
    """Process all text files in the specified directory."""
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):  # Assuming you're working with text files
            file_path = os.path.join(directory, filename)
            title, name, id_ = extract_info_from_file(file_path)

            if title and name and id_:
                new_file_name = generate_file_name(title, name, id_)
                new_file_path = os.path.join(directory, new_file_name)
                os.rename(file_path, new_file_path)
                print(f"Renamed '{filename}' to '{new_file_name}'")
            else:
                print(f"Could not extract all information from '{filename}'")

# Run the process on a specified directory
process_files_in_directory("path/to/your/files")