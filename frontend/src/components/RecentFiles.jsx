import { FileText } from "lucide-react";
import { getRecentFiles } from "../services/api";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
function RecentFiles() {
  const [files, setFiles] = useState([]);
  const navigate = useNavigate();

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
    <div className="card-bg rounded-2xl p-6 shadow-lg">
      <h2 className="mb-5 text-xl font-semibold text-theme">
        Recent Files
      </h2>

      <div className="space-y-3">
        {files.length === 0 ? (
            <p className="text-theme opacity-70">
              No recent files found.
            </p>
          ) : (
            files.slice(0, 5).map((file) => (
              <div
                key={file.id}
                className="flex items-center gap-3 rounded-xl border-theme p-4 transition hover:border-cyan-400 hover:opacity-80"
              >
                <FileText size={20} className="text-cyan-400" />

                <span className="text-theme">
                  {file.name}
                </span>
              </div>
            ))
          )}
        
      </div>
      <div className="mt-5 flex justify-end">
        <button
          onClick={() => navigate("/recent")}
          className="text-cyan-400 hover:text-cyan-300 font-medium transition"
        >
          View More →
        </button>
      </div>
    </div>
  );
}

export default RecentFiles;