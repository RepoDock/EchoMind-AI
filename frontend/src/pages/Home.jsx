import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import SearchBar from "../components/SearchBar";
import FolderButton from "../components/FolderButton";
import StatsCard from "../components/StatsCard";
import RecentFiles from "../components/RecentFiles";
import { useEffect } from "react";
import api from "../services/api";
function Home() {
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
}, []);
  return (
    <div className="min-h-screen bg-slate-950 flex">
      <Sidebar />

      <main className="flex-1 p-10">
        <Header />

        <SearchBar />

        <FolderButton />

        <div className="grid grid-cols-3 gap-6 my-8">
          <StatsCard title="Files" value="0" />
          <StatsCard title="Folders" value="0" />
          <StatsCard title="Indexed" value="0%" />
        </div>

        <RecentFiles />
      </main>
    </div>
  );
}

export default Home;