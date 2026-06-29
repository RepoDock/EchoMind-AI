import { Search } from "lucide-react";

function SearchBar() {
  return (
    <div className="relative mb-6">
      <Search
        size={20}
        className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"
      />

      <input
        type="text"
        placeholder="Search your memory..."
        className="w-full rounded-xl border border-slate-700 bg-slate-900 py-4 pl-12 pr-4 text-white placeholder:text-slate-400 outline-none transition focus:border-cyan-400"
      />
    </div>
  );
}

export default SearchBar;