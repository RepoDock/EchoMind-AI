import { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import { getFolder, saveFolder } from "../services/api";

function Settings() {
  const [folder, setFolder] = useState("");

  useEffect(() => {
    getFolder()
      .then((response) => {
        setFolder(response.data.folder);
      })
      .catch(console.error);
  }, []);

  const handleFolder = async () => {
    const newFolder = prompt("Enter Folder Path", folder);

    if (!newFolder) return;

    try {
      await saveFolder(newFolder);

      setFolder(newFolder);

      alert("✅ Folder Saved Successfully");
    } catch (err) {
      console.error(err);
      alert("❌ Failed to Save Folder");
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex">
      <Sidebar />

      <main className="flex-1 p-10 text-white">

        <h1 className="text-4xl font-bold mb-8">
          Settings
        </h1>

        <div className="bg-slate-900 border border-slate-700 rounded-xl p-6">

          <h2 className="text-2xl font-semibold mb-4">
            📂 Default Scan Folder
          </h2>

          <p className="text-slate-400 break-all">
            {folder || "No Folder Selected"}
          </p>

          <button
            onClick={handleFolder}
            className="mt-6 bg-cyan-500 hover:bg-cyan-600 px-5 py-3 rounded-lg"
          >
            Change Folder
          </button>

        </div>

        <div className="bg-slate-900 border border-slate-700 rounded-xl p-6 mt-8">

          <h2 className="text-2xl font-semibold">
            ℹ️ About EchoMind
          </h2>

          <div className="mt-4 space-y-2 text-slate-300">

            <p>Version : 0.1 Alpha</p>

            <p>Backend : FastAPI</p>

            <p>Database : SQLite</p>

            <p>AI Model : Phi-3 Mini</p>

          </div>

        </div>

      </main>
    </div>
  );
}

export default Settings;