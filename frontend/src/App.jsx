import {
  BrowserRouter,
  HashRouter,
  Routes,
  Route
} from "react-router-dom";
import DocumentAI from "./pages/DocumentAI";
import Home from "./pages/Home";
import Documents from "./pages/Documents";
import Recent from "./pages/Recents";
import Settings from "./pages/Settings";
import AIChat from "./pages/AIChat";
import Setup from "./pages/Setup";
const Router =
  window.location.protocol === "file:"
    ? HashRouter
    : BrowserRouter;

function App() {
  return (
    <Router>

      <Routes>
        <Route
          path="/setup"
          element={<Setup />}
        />
        <Route path="/" element={<Home />} />
        <Route path="/documents" element={<Documents />} />
        <Route path="/recent" element={<Recent />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/ai-chat" element={<AIChat />} />
        <Route
          path="/document-ai/:id"
          element={<DocumentAI />}
        />
      </Routes>
    </Router>
  );
}

export default App;