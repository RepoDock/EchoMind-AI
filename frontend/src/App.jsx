import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Documents from "./pages/Documents";
import Recent from "./pages/Recents";
import Settings from "./pages/Settings";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/documents" element={<Documents />} />
        <Route path="/recent" element={<Recent />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;