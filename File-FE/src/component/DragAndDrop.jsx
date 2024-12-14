import React, { useState } from "react";

export default function DragAndDrop() {
  const [droppedFiles, setDroppedFiles] = useState([]);

  const handleDrop = (event) => {
    event.preventDefault();
    const items = event.dataTransfer.items;

    let files = [];
    if (items) {
      for (let i = 0; i < items.length; i++) {
        const item = items[i].webkitGetAsEntry();
        if (item) {
          traverseFileTree(item, files);
        }
      }
    } else {
      const fileList = event.dataTransfer.files;
      for (let i = 0; i < fileList.length; i++) {
        files.push(fileList[i].name);
      }
    }
  };

  const traverseFileTree = (item, fileList) => {
    if (item.isFile) {
      item.file((file) => {
        fileList.push(file.name);
        setDroppedFiles([...fileList]);
      });
    } else if (item.isDirectory) {
      const dirReader = item.createReader();
      dirReader.readEntries((entries) => {
        entries.forEach((entry) => traverseFileTree(entry, fileList));
      });
    }
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-r from-blue-500 via-purple-500 to-blue-500 text-white">
      <div
        className="flex flex-col justify-center items-center border-2 border-dashed border-white rounded-lg p-6 w-2/3 max-w-3xl bg-opacity-20 bg-white cursor-pointer hover:bg-opacity-30 transition-all"
        onDrop={handleDrop}
        onDragOver={handleDragOver}
      >
        <p className="text-lg font-bold">Drag and Drop Files or Folders Here</p>
        <p className="text-sm mt-2">(Supports multiple files and folders)</p>
      </div>
      <div className="mt-6 w-2/3 max-w-3xl bg-white bg-opacity-10 rounded-lg p-4">
        <h3 className="text-lg font-semibold border-b pb-2 mb-4">Uploaded Files</h3>
        {droppedFiles.length === 0 ? (
          <p className="text-gray-300">No files uploaded yet</p>
        ) : (
          <ul className="list-disc ml-6 space-y-2">
            {droppedFiles.map((file, index) => (
              <li key={index} className="text-white text-sm">
                {file}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}