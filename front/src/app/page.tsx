import DisplayReceipts from "@/components/DisplayReceipts";
import DragAndDrop from "@/components/DragAndDrop";
import UploadButton from "@/components/UploadButton";
import { FiPlus } from "react-icons/fi";

export default function Home() {
  
  return (
    <div className="p-2">
      <UploadButton/>
      <DragAndDrop />
      <DisplayReceipts />
    </div>
  );
}
