import Header from "../components/Header";
import SearchBar from "../components/SearchBar";
import FolderButton from "../components/FolderButton";
import StatsCard from "../components/StatsCard";

function Home() {
  return (
    <div>
      <Header />

      <SearchBar />

      <FolderButton />

      <StatsCard />
    </div>
  );
}

export default Home;