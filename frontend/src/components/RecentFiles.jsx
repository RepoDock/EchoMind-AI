import { FileText } from "lucide-react";

function RecentFiles() {
  const files = [
    "DBMS Notes.pdf",
    "React Guide.docx",
    "AI Research.pdf",
  ];

  return (
    <div className="card-bg rounded-2xl p-6 shadow-lg">
      <h2 className="mb-5 text-xl font-semibold text-theme">
        Recent Files
      </h2>

      <div className="space-y-3">
        {files.map((file, index) => (
          <div
            key={index}
            className="flex items-center gap-3 rounded-xl border-theme p-4 transition hover:border-cyan-400 hover:opacity-80"
          >
            <FileText size={20} className="text-cyan-400" />

            <span className="text-theme">
              {file}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default RecentFiles;