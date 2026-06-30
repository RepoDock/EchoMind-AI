import { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import { useTheme } from "../theme/ThemeContext";
import { themes } from "../theme/themes";
import {
  getFolder,
  saveFolder,
  browseFolder,
  clearData,
} from "../services/api";
function Settings() {
  const [folder, setFolder] = useState("");
  const { theme, setTheme } = useTheme();
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

    alert("✅ Folder Saved Successfully");

  } catch (err) {

    console.error(err);

    alert("❌ Failed to Save Folder");

  }

};
const handleClearData = async () => {

  const confirmClear = window.confirm(
    "Delete all indexed documents and app data?"
  );

  if (!confirmClear) return;

  try {

    await clearData();

    alert("✅ App data cleared.");

  } catch (err) {

    console.error(err);

    alert("❌ Failed to clear app data.");

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
      onClick={() => {
        if (
          window.confirm("Delete all AI chat history?")
        ) {
          localStorage.removeItem("echomind_chats");

          alert("✅ Chat history deleted.");
        }
      }}
      className="bg-red-500 hover:bg-red-600 px-5 py-3 rounded-lg"
    >
      Clear Chat History
    </button>

    <button
      onClick={handleClearData}
      className="bg-orange-500 hover:bg-orange-600 px-5 py-3 rounded-lg"
    >
      Clear App Data
    </button>

  </div>

</div>
 
        <div className="card-bg rounded-xl p-6 mt-8">
          <h2 className="text-2xl font-semibold">
            ℹ️ About EchoMind
          </h2>

          <div className="mt-4 space-y-2 text-theme opacity-80">

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