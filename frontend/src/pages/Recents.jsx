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
    <div className="min-h-screen bg-slate-950 flex">
      <Sidebar />

      <main className="flex-1 p-10 text-white">

        <h1 className="text-4xl font-bold mb-3">
          Recent Files
        </h1>

        <p className="text-slate-400 mb-8">
          Last 10 indexed documents
        </p>

        <div className="space-y-5">

          {files.map((file) => (
            <div
              key={file.id}
              className="bg-slate-900 border border-slate-700 rounded-xl p-6 hover:border-cyan-400 transition"
            >
              <h2 className="text-2xl font-semibold">
                📄 {file.name}
              </h2>

              <p className="text-slate-400 mt-2 break-all">
                {file.path}
              </p>

              <div className="flex gap-8 mt-4 text-slate-300">
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