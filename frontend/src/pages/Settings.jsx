import { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import { useTheme } from "../theme/ThemeContext";
import { themes } from "../theme/themes";
import ConfirmModal from "../components/ui/ConfirmModal";
import { useToast } from "../context/ToastContext";
import {
  getFolder,
  saveFolder,
  browseFolder,
  clearData,
} from "../services/api";
function Settings() {
  const [showClearChatModal, setShowClearChatModal] = useState(false);
  const [showClearDataModal, setShowClearDataModal] = useState(false);
  const [folder, setFolder] = useState("");
  const { theme, setTheme } = useTheme();
  const { showToast } = useToast();
  useEffect(() => {
    getFolder()
      .then((response) => {
        setFolder(response.data.folder);
      })
      .catch(console.error);
  }, []);

const handleFolder = async () => {

  try {

    const response = await browseFolder();

    const newFolder = response.data.folder;

    if (!newFolder) return;

    await saveFolder(newFolder);

    setFolder(newFolder);

    showToast("Folder Saved Successfully");

  } catch (err) {

    console.error(err);


    showToast("Failed to Save Folder", "error");

  }

};
const handleClearData = async () => {

  try {

    await clearData();

    showToast("App Data Cleared Successfully");

  } catch (err) {

    console.error(err);
    showToast("Failed to clear data", "error");
    

  }

};
  return (
    <div className="min-h-screen app-bg flex">
      <Sidebar />

      <main className="flex-1 p-10 text-theme">

        <h1 className="text-4xl font-bold mb-8">
          Settings
        </h1>

        <div className="card-bg rounded-xl p-6">

          <h2 className="text-2xl font-semibold mb-4">
            📂 Default Scan Folder
          </h2>

          <p className="text-theme opacity-70 break-all">
            {folder || "No Folder Selected"}
          </p>

          <button
            onClick={handleFolder}
            className="mt-6 bg-cyan-500 hover:bg-cyan-600 px-5 py-3 rounded-lg"
          >
            Change Folder
          </button>

        </div>
        <div className="card-bg rounded-xl p-6 mt-8">

          <h2 className="text-2xl font-semibold mb-4">
            🎨 Appearance
          </h2>

          <p className="text-theme opacity-70 mb-5">
            Choose your preferred theme.
          </p>

          <div className="grid grid-cols-2 gap-4 mt-5">

            {Object.entries(themes).map(([key, item]) => (

              <button
                key={key}
                onClick={() => setTheme(key)}
                className={`rounded-xl p-4 border transition text-left ${
                  theme === key
                    ? "border-cyan-400 bg-cyan-500/10"
                    : "border-theme hover:opacity-80"
                }`}
              >
                <div className="font-semibold">
                  {item.name}
                </div>

                <div className="text-sm text-theme opacity-70 mt-1">
                  {key}
                </div>

              </button>

            ))}

          </div>

        </div>

            <div className="card-bg rounded-xl p-6 mt-8">

  <h2 className="text-2xl font-semibold mb-4">
    🗑 Storage
  </h2>

  <p className="text-theme opacity-70 mb-6">
    Manage your saved chats and indexed data.
  </p>

  <div className="flex gap-4 flex-wrap">

    <button
      onClick={() => 
        setShowClearChatModal(true)
      }
      className="bg-red-500 hover:bg-red-600 px-5 py-3 rounded-lg"
    >
      Clear Chat History
    </button>

    <button
      onClick={() => setShowClearDataModal(true)}
      className="bg-orange-500 hover:bg-orange-600 px-5 py-3 rounded-lg"
    >
      Clear App Data
    </button>

  </div>

</div>
 
        <div className="card-bg rounded-xl p-6 mt-8">
          <h2 className="text-2xl font-semibold">
            ℹ️ About AXON
          </h2>

          <div className="mt-4 space-y-2 text-theme opacity-80">

            <p>Version : 0.1 Alpha</p>

            <p>Backend : FastAPI</p>

            <p>Database : SQLite</p>

            <p>AI Model : Phi-3 Mini</p>

          </div>

        </div>

      </main>
      <ConfirmModal
            open={showClearChatModal}
            title="Delete Chat History"
            message="This will permanently delete all AI chat history."
            confirmText="Delete"
            onCancel={() => setShowClearChatModal(false)}
            onConfirm={() => {

              localStorage.removeItem("axon_chats");

              setShowClearChatModal(false);
              showToast("Chat Cleared");
              

              

            }}
          />

          <ConfirmModal
            open={showClearDataModal}
            title="Clear App Data"
            message="This will permanently delete indexed documents, embeddings and search history."
            confirmText="Clear"
            onCancel={() => setShowClearDataModal(false)}
            onConfirm={async () => {

              await handleClearData();

              setShowClearDataModal(false);

            }}
          />
          
    </div>
  );
}

export default Settings;