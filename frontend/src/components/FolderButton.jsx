import { FolderOpen } from "lucide-react";

function FolderButton() {
  return (
    <button
      className="mb-8 flex items-center gap-3 rounded-xl bg-cyan-500 px-6 py-4 font-semibold text-white transition hover:bg-cyan-600"
    >
      <FolderOpen size={20} />
      Select Folder
    </button>
  );
}

export default FolderButton;