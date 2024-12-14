from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import List
import os

app = FastAPI()

# Function to process a single file
def process_file(file: UploadFile):
    # Simulate extracting details from the file
    content = file.filename  # Here you would read and analyze file content
    topic = "example_topic"
    student_id = "12345"
    name = "example_name"
    return {"originalName": file.filename, "newName": f"{topic}_{student_id}_{name}"}

@app.post("/process-files/")
async def process_files(files: List[UploadFile] = File(...)):
    processed_files = []
    for file in files:
        # Validate file type
        if not file.filename.endswith((".pdf", ".docx")):
            return JSONResponse({"error": f"Invalid file type: {file.filename}"}, status_code=400)

        # Process file and append result
        processed_files.append(process_file(file))

    return JSONResponse(processed_files)

dist_directory = os.path.join(os.getcwd(), "../File-FE/dist")
app.mount("/", StaticFiles(directory= dist_directory, html=True), name="static")

# Example root route for testing
@app.get("/api/")
async def root():
    return {"message": "FastAPI backend for file-naming system"}