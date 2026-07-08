import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import {
  getFiles,
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

function Documents() {
  const navigate = useNavigate();
    const [sortBy, setSortBy] = useState("name-asc");
  const [files, setFiles] = useState([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    getFiles()
      .then((response) => {
        setFiles(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

 const filteredFiles = files
  .filter((file) =>
    file.name.toLowerCase().includes(search.toLowerCase())
  )
  .sort((a, b) => {
    switch (sortBy) {
      case "name-asc":
        return a.name.localeCompare(b.name);

      case "name-desc":
        return b.name.localeCompare(a.name);

      case "size-asc":
        return a.size - b.size;

      case "size-desc":
        return b.size - a.size;

      case "type":
        return a.extension.localeCompare(b.extension);

      default:
        return 0;
    }
  });

  return (

        <div className="min-h-screen app-bg flex overflow-hidden">
      <Sidebar />

        <main className="flex-1 min-w-0 p-10 text-theme overflow-x-hidden">

        <h1 className="text-4xl font-bold mb-8">
          Documents
        </h1>

<div className="grid grid-cols-[1fr_220px] gap-4 mb-8">

  <div className="flex-1">
    <input
      type="text"
      placeholder="🔍 Search documents..."
      value={search}
      onChange={(e) => setSearch(e.target.value)}
      className="w-full card-bg rounded-xl p-4 outline-none focus:border-cyan-400"
    />
  </div>

  <select
    value={sortBy}
    onChange={(e) => setSortBy(e.target.value)}
    className="w-52 flex-shrink-0 card-bg rounded-xl p-4 text-theme"
  >
    <option value="name-asc">📄 Name (A-Z)</option>
    <option value="name-desc">📄 Name (Z-A)</option>
    <option value="size-asc">📦 Size ↑</option>
    <option value="size-desc">📦 Size ↓</option>
    <option value="type">📁 File Type</option>
    <option value="recent">🕒 Recently Modified</option>
  </select>



</div>

        <p className="text-theme opacity-70 mb-6">
          {filteredFiles.length} Documents Found
        </p>

        <div className="space-y-5">

          {filteredFiles.map((file) => (
            <div
              key={file.id}
              className="card-bg rounded-xl p-6 hover:border-cyan-400 transition-all"
            >
              <h2 className="text-2xl font-semibold">
                📄 {file.name}
              </h2>

              
             <p className="text-theme opacity-70 mt-2 break-words overflow-hidden">
                {file.path}
            </p>

              <div className="flex gap-8 mt-4 text-theme opacity-80">
                <span>
                  <strong>Type:</strong> {file.extension}
                </span>

                <span>
                  <strong>Size:</strong> {formatSize(file.size)}
                </span>
              </div>
                <div className="flex gap-4 mt-6">

                <button
                    onClick={() => openFile(file.path)}
                    className="bg-cyan-500 hover:bg-cyan-600 px-5 py-2 rounded-lg transition"
                >
                    📂 Open
                </button>

                <button
                    onClick={() => showInFolder(file.path)}
                    className="bg-slate-700 hover:bg-slate-600 px-5 py-2 rounded-lg transition"
                >
                    📁 Show in Folder
                </button>
                <button
                  onClick={() => navigate(`/document-ai/${file.id}`)}
                  className="bg-violet-600 hover:bg-violet-700 px-5 py-2 rounded-lg transition"
                >
                  ✨ Ask AI
                </button>

                </div>
              

            </div>
          ))} 

        </div>

      </main>
    </div>
  );
}

export default Documents;