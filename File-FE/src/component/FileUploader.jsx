import React, { useRef } from "react";

export default function FileUploader({ addFiles }) {
  const fileInputRef = useRef();

  // Handle file drop
  const handleDrop = async (event) => {
    event.preventDefault();

    const items = event.dataTransfer.items;
    let files = [];

    if (items) {
      for (let i = 0; i < items.length; i++) {
        const item = items[i].webkitGetAsEntry();
        if (item) {
          await traverseFileTree(item, files);
        }
      }
    } else {
      const fileList = event.dataTransfer.files;
      for (let i = 0; i < fileList.length; i++) {
        if (isValidFile(fileList[i].name)) files.push(fileList[i].name);
      }
    }

    addFiles(files);
  };

  // Recursive function to process folders and files
  const traverseFileTree = (item, fileList) =>
    new Promise((resolve) => {
      if (item.isFile) {
        item.file((file) => {
          if (isValidFile(file.name)) fileList.push(file.name);
          resolve();
        });
      } else if (item.isDirectory) {
        const dirReader = item.createReader();
        dirReader.readEntries(async (entries) => {
          for (const entry of entries) {
            await traverseFileTree(entry, fileList);
          }
          resolve();
        });
      }
    });

  // Validate file extensions
  const isValidFile = (fileName) => /\.(pdf|docx|txt)$/i.test(fileName);

  // Handle manual file upload
  const handleFileInputChange = (event) => {
    const files = Array.from(event.target.files).filter((file) =>
      isValidFile(file.name)
    );
    const fileNames = files.map((file) => file.name);
    addFiles(fileNames);
    fileInputRef.current.value = ""; // Reset the input
  };

  // Open file input dialog
  const handleClick = () => fileInputRef.current.click();

  return (
    <div
      className="flex flex-col justify-center items-center border-2 border-dashed border-gray-300 rounded-lg shadow-md p-6 w-2/3 max-w-3xl bg-white cursor-pointer hover:shadow-lg transition-all"
      onDrop={handleDrop}
      onDragOver={(e) => e.preventDefault()}
      onClick={handleClick}
    >
      <input
        ref={fileInputRef}
        type="file"
        multiple
        className="hidden"
        onChange={handleFileInputChange}
      />
      <p className="text-lg font-semibold text-gray-600">Drag and Drop Files or Folders Here</p>
      <p className="text-sm text-gray-400 mt-1">Supports .pdf, .docx, and .txt</p>
      <p className="text-sm text-gray-400 mt-1">(Click to browse files)</p>
    </div>
  );
}

