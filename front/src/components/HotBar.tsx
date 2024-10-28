"use client";

import { useModelStore } from "@/store/UiStore";

export default function HotBar() {
  const { model, setModel } = useModelStore();

  return (
    <>
      <div className=" flex  text-black w-full justify-end">
        <select value={model} onChange={(e) => setModel(e.target.value)}>
          <option value="minicpm">MiniCPM V2.6</option>
          <option value="minicpm-gguf">MiniCPM V2.6 (CPU)</option>
          <option value="donut">Donut</option>
          <option disabled value="udop">
            UDOP
          </option>
        </select>
      </div>
    </>
  );
}
