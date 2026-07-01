import { Search } from "lucide-react";
import { useState } from "react";

function SearchBar({ onSearch }) {

  const [query, setQuery] = useState("");

  const handleSearch = (e) => {

    if (e.key === "Enter" && query.trim()) {

      onSearch(query);

    }

  };

return (
  <div className="flex mb-6">

    <div className="relative flex-1">

      <Search
        size={20}
        className="absolute left-4 top-1/2 -translate-y-1/2 text-theme opacity-60"
      />

      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={handleSearch}
        placeholder="Ask anything about your documents..."
        className="w-full card-bg rounded-l-xl py-4 pl-12 pr-4 text-theme placeholder:text-theme placeholder:opacity-60 outline-none transition focus:border-cyan-400"
      />

    </div>

    <button
      onClick={() => {

        if (query.trim()) {

          onSearch(query);

        }

      }}
      className="px-6 bg-cyan-500 hover:bg-cyan-600 text-white rounded-r-xl transition"
    >
      <div className="flex items-center gap-2">
        <Search size={18} />
        <span>Search</span>
      </div>
    </button>

  </div>
);
}

export default SearchBar;