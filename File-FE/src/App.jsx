import React, { useState } from "react";
import FileUploader from "./component/FileUploader";
import FileList from "./component/FileList";
import './App.css';

export default function App() {
  const [files, setFiles] = useState([]);

  // Add files to the list
  const addFiles = (newFiles) => {
    setFiles((prevFiles) => [...prevFiles, ...newFiles]);
  };

  // Remove file from the list
  const removeFile = (index) => {
    setFiles((prevFiles) => prevFiles.filter((_, i) => i !== index));
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50">
      <h1 className="text-2xl font-bold text-purple-600 mb-4">File Uploader</h1>
      <FileUploader addFiles={addFiles} />
      <FileList files={files} removeFile={removeFile} />
    </div>
  );
}


