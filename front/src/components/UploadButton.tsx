import { FiPlus } from "react-icons/fi";

export default function UploadButton() {
  return (
    <div>
      <button className=" bg-orange-300 p-2 rounded-full border border-slate-400 border-solid hover:scale-110">
        <FiPlus fill="black" color="black" />
      </button>
    </div>
  );
}
