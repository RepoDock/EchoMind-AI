import { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import {
  getRecentFiles,
  openFile,
  showInFolder,
} from "../services/api";

const formatSize = (bytes) => {
  if (bytes < 1024) return bytes + " B";
  if (bytes < 1024 * 1024)
    return (bytes / 1024).toFixed(1) + " KB";
  if (bytes < 1024 * 1024 * 1024)
    return (bytes / (1024 * 1024)).toFixed(2) + " MB";

  return (bytes / (1024 * 1024 * 1024)).toFixed(2) + " GB";
};

function Recent() {
  const [files, setFiles] = useState([]);

  useEffect(() => {
    getRecentFiles()
      .then((response) => {
        setFiles(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  return (
    <div className="min-h-screen app-bg flex">
      <Sidebar />

      <main className="flex-1 p-10 text-theme">

        <h1 className="text-4xl font-bold mb-3">
          Recent Files
        </h1>

        <p className="text-theme opacity-70 mb-8">
          Last 10 indexed documents
        </p>

        <div className="space-y-5">

          {files.map((file) => (
            <div
              key={file.id}
              className="card-bg rounded-xl p-6 transition hover:border-cyan-400"
            >
              <h2 className="text-2xl font-semibold">
                📄 {file.name}
              </h2>

              <p className="text-theme opacity-70 mt-2 break-all">
                {file.path}
              </p>

              <div className="flex gap-8 mt-4 text-theme opacity-80">
                <span>
                  <strong>Type:</strong> {file.extension}
                </span>

                <span>
                  <strong>Size:</strong> {formatSize(file.size)}
                </span>

                <span>
                  <strong>Modified:</strong> {file.modified_at}
                </span>
              </div>

              <div className="flex gap-4 mt-6">

                <button
                  onClick={() => openFile(file.path)}
                  className="bg-cyan-500 hover:bg-cyan-600 px-5 py-2 rounded-lg"
                >
                  📂 Open
                </button>

                <button
                  onClick={() => showInFolder(file.path)}
                  className="bg-slate-700 hover:bg-slate-600 px-5 py-2 rounded-lg"
                >
                  📁 Show in Folder
                </button>

              </div>

            </div>
          ))}

        </div>

      </main>
    </div>
  );
}

export default Recent;