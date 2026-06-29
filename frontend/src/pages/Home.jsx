import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import SearchBar from "../components/SearchBar";
import FolderButton from "../components/FolderButton";
import StatsCard from "../components/StatsCard";
import RecentFiles from "../components/RecentFiles";
import { useEffect, useState } from "react";
import api, { getStats } from "../services/api";

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

        <SearchBar />

        <FolderButton onScanComplete={loadStats} />

        <div className="grid grid-cols-3 gap-6 my-8">
          <StatsCard title="Files" value={stats.files} />
          <StatsCard title="Folders" value={stats.folders} />
          <StatsCard title="Indexed" value={`${stats.indexed}%`} />
        </div>

        <RecentFiles />
      </main>
    </div>
  );
}

export default Home;