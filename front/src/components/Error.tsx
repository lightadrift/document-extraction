"use client";
import { useErrorStore } from "@/store/UiStore";

export default function ErrorBox() {
  const store = useErrorStore();
  return (
    <>
      {store.error != "" ? (
        <div className=" text-black bg-red-300 w-fit ml-4 p-2">
          {store.error}
        </div>
      ) : null}
    </>
  );
}
