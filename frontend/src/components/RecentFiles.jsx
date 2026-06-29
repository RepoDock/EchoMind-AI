import { FileText } from "lucide-react";

function RecentFiles() {
  const files = [
    "DBMS Notes.pdf",
    "React Guide.docx",
    "AI Research.pdf",
  ];

  return (
    <div className="rounded-2xl border border-slate-700 bg-slate-900 p-6 shadow-lg">
      <h2 className="mb-5 text-xl font-semibold text-white">
        Recent Files
      </h2>

      <div className="space-y-3">
        {files.map((file, index) => (
          <div
            key={index}
            className="flex items-center gap-3 rounded-xl border border-slate-700 p-4 transition hover:border-cyan-400 hover:bg-slate-800"
          >
            <FileText size={20} className="text-cyan-400" />

            <span className="text-slate-200">
              {file}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default RecentFiles;