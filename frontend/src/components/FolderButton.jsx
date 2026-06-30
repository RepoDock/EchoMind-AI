import { useState } from "react";
import { scanFolder, getScanFolder } from "../services/api";
import { Folder } from "lucide-react";
import { useToast } from "../context/ToastContext";
function FolderButton({ onScanComplete }) {
  const [loading, setLoading] = useState(false);
  const { showToast } = useToast();

const handleScan = async () => {
  try {
    setLoading(true);

    // Settings me saved folder lo
    const folderResponse = await getScanFolder();
    const folderPath = folderResponse.data.folder;


    if (!folderPath) {
      showToast("Please select a folder in Settings first.", "error");
      return;
    }

    // Scan start
    const response = await scanFolder(folderPath);

    console.log("Scanner Response:", response.data);

    showToast(
      `Indexed ${response.data.files_indexed} files`
    );

    // Home stats refresh
    if (onScanComplete) {
      onScanComplete();
    }

  } catch (error) {
    console.error(error);
    showToast("Scan Failed", "error");
  } finally {
    setLoading(false);
  }
};

  return (
    <>
  <button
    onClick={handleScan}
    disabled={loading}
    className="
      flex
      items-center
      gap-3
      bg-cyan-500
      hover:bg-cyan-600
      text-white
      px-6
      py-4
      rounded-xl
      font-semibold
      transition
      disabled:opacity-60
    "
  >
    <Folder size={22} />

    {loading ? "Scanning..." : "📂 Scan Folder"}
  </button>

  {loading && (
    <div className="mt-4 card-bg rounded-xl p-4">
      <p className="text-cyan-400 font-semibold animate-pulse">
        🔄 AI is indexing your files...
      </p>

      <p className="text-theme opacity-70 mt-2">
        Please wait while EchoMind extracts text and creates embeddings.
      </p>
    </div>
  )}
</>
    // <button
    //   onClick={handleScan}
    //   disabled={loading}
    //   className="
    //     flex
    //     items-center
    //     gap-3
    //     bg-cyan-500
    //     hover:bg-cyan-600
    //     text-white
    //     px-6
    //     py-4
    //     rounded-xl
    //     font-semibold
    //     transition
    //     disabled:opacity-60
    //   "
    // >
    //   <Folder size={22} />

    //   {loading ? "Scanning..." : "📂 Scan Folder"}
    // </button>
  );
}

export default FolderButton;