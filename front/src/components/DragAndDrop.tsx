"use client";

import { useReceiptStore } from "@/store/ReceiptsStore";
import { useErrorStore, useModelStore } from "@/store/UiStore";
import { useReducer } from "react";
import { MdClear } from "react-icons/md";

type Action =
  | { type: "SET_FILES"; payload: File[] }
  | { type: "REMOVE_FILE"; payload: number }
  | { type: "CLEAR_FILES" }
  | { type: "SET_UPLOADING"; payload: boolean }
  | { type: "SET_DRAGGING"; payload: boolean };

interface State {
  files: File[];
  uploading: boolean;
  isDragging: boolean;
}

const initialState: State = {
  files: [],
  uploading: false,
  isDragging: false,
};

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case "SET_FILES":
      return { ...state, files: [...state.files, ...action.payload] };
    case "REMOVE_FILE":
      return {
        ...state,
        files: state.files.filter((_, i) => i !== action.payload),
      };
    case "CLEAR_FILES":
      return { ...state, files: [] };
    case "SET_UPLOADING":
      return { ...state, uploading: action.payload };
    case "SET_DRAGGING":
      return { ...state, isDragging: action.payload };
    default:
      return state;
  }
}

export default function DragAndDrop() {
  const [state, dispatch] = useReducer(reducer, initialState);
  const receip_store = useReceiptStore();
  const model_store = useModelStore();
  const { setError } = useErrorStore();
  const handleSendFiles = async () => {
    dispatch({ type: "SET_UPLOADING", payload: true });
    const formData = new FormData();
    const modelName = model_store.model;

    state.files.forEach((file) => {
      formData.append("files", file);
    });

    try {
      const response = await fetch("http://127.0.0.1:3001/parser", {
        method: "POST",
        headers: {
          "X-Model-Name": modelName, // Custom header pro servidor
        },
        body: formData,
      });
      const jsonData = await response.json();
      if (response.ok) {
        console.log("ok")
        console.log(jsonData.data, "aqui")
        receip_store.updateListReceipts(jsonData.data);
        dispatch({ type: "CLEAR_FILES" });
      } else {
        console.error("Error sending files:", response.status);
        console.error("Error message:", jsonData.error);
        setError(JSON.stringify(jsonData.error))

      }
    } catch (error) {
      console.error("Error sending files:", error);
    } finally {
      dispatch({ type: "SET_UPLOADING", payload: false });
    }
  };

  const handleDrop = (event: React.DragEvent<HTMLElement>) => {
    event.preventDefault();
    const droppedFiles = Array.from(event.dataTransfer.files);
    dispatch({ type: "SET_FILES", payload: droppedFiles });
  };

  const handleDragOver = (event: React.DragEvent<HTMLElement>) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = "copy";
  };

  const handleRemoveFile = (index: number) => {
    dispatch({ type: "REMOVE_FILE", payload: index });
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = event.target.files;
    if (selectedFiles && selectedFiles.length > 0) {
      const newFiles = Array.from(selectedFiles);
      dispatch({ type: "SET_FILES", payload: newFiles });
    }
  };

  const handleBrowseClick = () => {
    const fileInput = document.getElementById("fileInput");
    fileInput?.click();
  };

  return (
    <section
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      className="bg-zinc-900 w-[30vw] border border-slate-600 border-solid m-4 p-2 h-full relative font-geist"
    >
      <div className="h-40 gap-4">
        <input
          type="file"
          id="fileInput"
          style={{ display: "none" }}
          onChange={handleFileChange}
          multiple
        />
        <button
          className="bg-orange-300 p-2 rounded-sm text-black hover:scale-105"
          onClick={handleBrowseClick}
        >
          Browse Files
        </button>
      </div>
      <div>
        {state.files.length > 0 && (
          <div className="mb-2">
            {state.files.map((file, index) => (
              <div
                key={index}
                className="flex bg-green-300 p-1 rounded-md w-fit mb-1 text-black"
              >
                <div className="file-info">
                  <p>{file.name}</p>
                </div>
                <div className="flex">
                  <MdClear
                    className="hover:cursor-pointer"
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
      {state.files.length > 0 && (
        <div className="mb-2">
          <button
            disabled={state.uploading}
            className="bg-orange-300 p-2 rounded-sm text-black font-geist hover:scale-105"
            onClick={handleSendFiles}
          >
            Enviar
          </button>
          <button
            onClick={() => dispatch({ type: "CLEAR_FILES" })}
            className="bg-red-400 p-2 ml-2 rounded-sm text-black font-geist hover:scale-105"
          >
            Limpar tudo
          </button>
        </div>
      )}

      <p>{state.files.length} file(s) selected</p>
    </section>
  );
}
