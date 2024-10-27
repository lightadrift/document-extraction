import DisplayReceipts from "@/components/DisplayReceipts";
import Drag_and_drop from "@/components/Drag_and_drop";
import UploadButton from "@/components/UploadButton";
import { FiPlus } from "react-icons/fi";

export default function Home() {
  
  return (
    <div className="p-2">
      <UploadButton/>
      <Drag_and_drop />
      <DisplayReceipts />
    </div>
  );
}
