import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import SearchBar from "../components/SearchBar";
import FolderButton from "../components/FolderButton";
import StatsCard from "../components/StatsCard";
import RecentFiles from "../components/RecentFiles";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api, {
  getStats,
  aiSearch,
  openFile,
} from "../services/api";
function Home() {
  const navigate = useNavigate();
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
    <div className="min-h-screen app-bg flex">
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

  <p className="text-theme">
    Searching...
  </p>

) : currentQuery.trim() ? (

  <>
    <p className="text-theme opacity-70 mb-4">
      {searchResults.length === 0
        ? "No files found"
        : `${searchResults.length} file${
            searchResults.length > 1 ? "s" : ""
          } found`}
    </p>

    {searchResults.length > 0 && (
      <div className="space-y-4">

    {searchResults.map((file) => (

      <div
        key={file.id}
        className="card-bg rounded-xl p-5"
      >

        <h2 className="text-xl font-bold text-theme">
          📄 {file.name}
        </h2>

        <p className="text-theme opacity-70 break-all">
          {file.path}
        </p>

        <p className="text-cyan-400 mt-2">
          AI Match: {(file.score * 100).toFixed(1)}%
        </p>
        <p className="text-theme opacity-80 mt-2 italic"
         dangerouslySetInnerHTML={{
        __html: highlightText(file.snippet),
        }}

        />
        <div className="flex gap-3 mt-5">

          <button
            onClick={() => openFile(file.path)}
            className="bg-cyan-500 hover:bg-cyan-600 text-white px-4 py-2 rounded-lg transition"
          >
            📂 Open
          </button>
          <button
              onClick={() => navigate(`/document-ai/${file.id}`)}
              className="bg-violet-600 hover:bg-violet-700 text-white px-4 py-2 rounded-lg transition"
          >
              🤖 Ask AI
          </button>

        </div>
        

      </div>

            ))}
      </div>
    )}

  </>

) : (

  <RecentFiles />

)}
      </main>
    </div>
  );
}

export default Home;