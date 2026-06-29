import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import SearchBar from "../components/SearchBar";
import FolderButton from "../components/FolderButton";
import StatsCard from "../components/StatsCard";
import RecentFiles from "../components/RecentFiles";
import { useEffect, useState } from "react";
import api, { getStats, aiSearch } from "../services/api";
function Home() {
  const [stats, setStats] = useState({
    files: 0,
    folders: 0,
    indexed: 0,
  });

  const loadStats = () => {
    getStats()
      .then((response) => {
        setStats(response.data);
        console.log("Stats:", response.data);
      })
      .catch((error) => {
        console.error("Stats Error:", error);
      });
  };
  const [searchResults, setSearchResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  const [currentQuery, setCurrentQuery] = useState("");
  const handleSearch = async (query) => {
  setCurrentQuery(query);

  if (!query.trim()) {
    setSearchResults([]);
    return;
  }

  try {

    setIsSearching(true);

    const response = await aiSearch(query);

    setSearchResults(response.data);

  } catch (error) {

    console.error(error);

  } finally {

    setIsSearching(false);

  }

};
const highlightText = (text) => {

  if (!currentQuery) return text;
  const escapedQuery = currentQuery.replace(
  /[.*+?^${}()|[\]\\]/g,
  "\\$&"
  );

  const regex = new RegExp(`(${escapedQuery})`, "gi");

  return text.replace(
    regex,
    "<span class='text-cyan-400 font-bold'>$1</span>"
  );
};
  useEffect(() => {
    api
      .get("/")
      .then((response) => {
        console.log("Backend Connected ✅");
        console.log(response.data);
      })
      .catch((error) => {
        console.error("Backend Connection Failed ❌");
        console.error(error);
      });

    loadStats();
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 flex">
      <Sidebar />

      <main className="flex-1 p-10">
        <Header />

        <SearchBar onSearch={handleSearch} />
        

        <FolderButton onScanComplete={loadStats} />

        <div className="grid grid-cols-3 gap-6 my-8">
          <StatsCard title="Files" value={stats.files} />
          <StatsCard title="Folders" value={stats.folders} />
          <StatsCard title="Indexed" value={`${stats.indexed}%`} />
        </div>

        {isSearching ? (

  <p className="text-white">
    Searching...
  </p>

) : searchResults.length > 0 ? (

  <div className="space-y-4">

    {searchResults.map((file) => (

      <div
        key={file.id}
        className="bg-slate-900 border border-slate-700 rounded-xl p-5"
      >

        <h2 className="text-xl font-bold text-white">
          📄 {file.name}
        </h2>

        <p className="text-slate-400 break-all">
          {file.path}
        </p>

        <p className="text-cyan-400 mt-2">
          AI Match: {(file.score * 100).toFixed(1)}%
        </p>
        <p className="text-slate-300 mt-2 italic"
         dangerouslySetInnerHTML={{
        __html: highlightText(file.snippet),
        }}

        />

      </div>

    ))}

  </div>

) : (

  <RecentFiles />

)}
      </main>
    </div>
  );
}

export default Home;