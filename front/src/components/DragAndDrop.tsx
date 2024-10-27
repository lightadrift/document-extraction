"use client";

import { useReceiptStore } from "@/store/ReceiptsStore";
import { useEffect, useState } from "react";
import { AiOutlineCheckCircle } from "react-icons/ai";
import { MdClear } from "react-icons/md";

export default function DragAndDrop() {
  const [uploading, setUploading] = useState(false);
  const [files, setFiles] = useState<File[]>([]);
  const store = useReceiptStore();

  const handleSendFiles = async () => {
    setUploading(true);
    const formData = new FormData();
    files.forEach((file) => {
      formData.append("files", file);
    });

    try {
      const response = await fetch("http://127.0.0.1:3001/parser", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        console.log("Files sent successfully!");
        const jsonData = await response.json();
        store.updateListReceipts(jsonData.data);
        setFiles([])
      } else {
        console.error("Error sending files:", response.status);
      }
    } catch (error) {
      console.error("Error sending files:", error);
    } finally {
      setUploading(false);
    }
  };

  const handleDragOver = (event: React.DragEvent<HTMLElement>) => {
    event.preventDefault(); // Prevent default behavior to allow drop
    event.dataTransfer.dropEffect = 'copy'; // Indicate a copy operation
  };

  const handleDrop = (event: React.DragEvent<HTMLElement>) => {
    event.preventDefault();
    const droppedFiles = event.dataTransfer.files;
    if (droppedFiles.length > 0) {
      const newFiles = Array.from(droppedFiles);
      setFiles((prevFiles) => [...prevFiles, ...newFiles]);
    }
  };

  const handleRemoveFile = (index: number) => {
    setFiles((prevFiles) => prevFiles.filter((_, i) => i !== index));
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = event.target.files;
    if (selectedFiles && selectedFiles.length > 0) {
      const newFiles = Array.from(selectedFiles);
      setFiles((prevFiles) => [...prevFiles, ...newFiles]);
    }
  };

  const handleBrowseClick = () => {
    const fileInput = document.getElementById("fileInput")!;
    fileInput.click();
  };

  useEffect(() => {
    setFiles(files);
  }, [files, setFiles]);

  return (
    <section
      onDrop={handleDrop}

      onDragOver={handleDragOver}
      className=" bg-zinc-900 w-[30vw] border border-slate-600 border-solid m-4 p-2 h-full relative font-geist"
    >
      <div className=" h-40 gap-4">
        <input
          type="file"
          id="fileInput"
          style={{ display: "none" }}
          onChange={handleFileChange}
          multiple
        />
        <button
          className=" bg-orange-300 p-2 rounded-sm text-black "
          onClick={handleBrowseClick}
        >
          Browse Files
        </button>
      </div>
      <div>
        {files.length > 0 && (
          <div>
            {files.map((file, index) => (
              <div key={index} className=" flex">
                <div className="file-info">
                  <p>{file.name}</p>
                </div>
                <div className="flex">
                  <AiOutlineCheckCircle
                    className=" hover:cursor-pointer"
                    size={20}
                    style={{ color: "#6DC24B", marginRight: 1 }}
                  />
                  <MdClear
                    className=" hover:cursor-pointer"
                    fill="red"
                    size={20}
                    onClick={() => handleRemoveFile(index)}
                  />
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
      {files.length > 0 ? (
        <button
          disabled={uploading}
          className="bg-orange-300 p-2 rounded-sm text-black font-geist"
          onClick={handleSendFiles}
        >
          Send Files
        </button>
      ) : null}

      <p>{files.length} file(s) selected </p>
    </section>
  );
}
