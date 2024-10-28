import DisplayReceipts from "@/components/DisplayReceipts";
import DragAndDrop from "@/components/DragAndDrop";
import ErrorBox from "@/components/Error";
import HotBar from "@/components/HotBar";
import UploadButton from "@/components/UploadButton";

export default function Home() {
  
  return (
    <div className="p-2">
      <HotBar/>
      {/* <UploadButton/> */}
      <DragAndDrop />
      <ErrorBox/>
      <DisplayReceipts />
    </div>
  );
}
