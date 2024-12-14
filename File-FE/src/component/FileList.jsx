import React from "react";

export default function FileList({ files, removeFile }) {
  return (
    <div className="w-2/3 max-w-3xl mt-4">
      {files.length === 0 ? (
        <p className="text-gray-500 text-sm">No files uploaded yet.</p>
      ) : (
        <ul className="space-y-2">
          {files.map((file, index) => (
            <li
              key={index}
              className="flex justify-between items-center border rounded-md px-3 py-2 shadow-sm bg-gray-100"
            >
              <span className="text-gray-700">{file}</span>
              <button
                onClick={() => removeFile(index)}
                className="text-red-500 hover:text-red-700 font-semibold text-sm"
              >
                Delete
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
