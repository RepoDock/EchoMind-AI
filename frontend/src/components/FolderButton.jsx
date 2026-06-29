import { useState } from "react";
import { scanFolder, getScanFolder } from "../services/api";
import { Folder } from "lucide-react";
function FolderButton({ onScanComplete }) {
  const [loading, setLoading] = useState(false);

const handleScan = async () => {
  try {
    setLoading(true);

    // Settings me saved folder lo
    const folderResponse = await getScanFolder();
    const folderPath = folderResponse.data.folder;

    if (!folderPath) {
      alert("⚠ Please select a folder in Settings first.");
      return;
    }

    // Scan start
    const response = await scanFolder(folderPath);

    console.log("Scanner Response:", response.data);

    alert(`✅ Indexed ${response.data.files_indexed} files`);

    // Home stats refresh
    if (onScanComplete) {
      onScanComplete();
    }

  } catch (error) {
    console.error(error);
    alert("❌ Scan Failed");
  } finally {
    setLoading(false);
  }
};

  return (
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
  );
}

export default FolderButton;