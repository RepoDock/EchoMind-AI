import { Search } from "lucide-react";
import { useState } from "react";

function SearchBar({ onSearch }) {

  const [query, setQuery] = useState("");

  const handleSearch = (e) => {

    if (e.key === "Enter") {
      onSearch(query);
    }

  };

  return (
    <div className="relative mb-6">

      <Search
        size={20}
       className="absolute left-4 top-1/2 -translate-y-1/2 text-theme opacity-60"
      />

      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={handleSearch}
        placeholder="Search your memory..."
        className="w-full card-bg rounded-xl py-4 pl-12 pr-4 text-theme placeholder:text-theme placeholder:opacity-60 outline-none transition focus:border-cyan-400"
      />

    </div>
  );
}

export default SearchBar;