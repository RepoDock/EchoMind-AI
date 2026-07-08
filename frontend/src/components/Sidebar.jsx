import {
  Home,
  FolderOpen,
  Clock3,
  Settings,
  Brain,
  MessageSquare,
} from "lucide-react";

import { NavLink } from "react-router-dom";

function Sidebar() {
  const linkClass = ({ isActive }) =>
    `flex items-center gap-3 w-full rounded-xl p-3 transition-all duration-200 ${
      isActive
        ? "bg-cyan-500/20 text-cyan-400"
        : "text-theme hover:opacity-80"
    }`;

  return (
    <aside className="w-64 card-bg border-r flex flex-col p-6">

      <div className="flex items-center gap-3 mb-12">

        <Brain size={34} className="text-cyan-400" />

        <div>
          <h1 className="text-2xl font-bold text-theme">
            AXON
          </h1>

          <p className="text-theme text-sm opacity-70">
            Your Personal AI Memory
            <br />
            v0.1.1 Alpha
          </p>
        </div>

      </div>

      <nav className="space-y-3">

        <NavLink to="/" className={linkClass}>
          <Home size={20} />
          Home
        </NavLink>

        <NavLink to="/documents" className={linkClass}>
          <FolderOpen size={20} />
          Documents
        </NavLink>

        <NavLink to="/recent" className={linkClass}>
          <Clock3 size={20} />
          Recent
        </NavLink>
        
        <NavLink to="/ai-chat" className={linkClass}>
          <MessageSquare size={20} />
          AI Chat
        </NavLink>

        <NavLink to="/settings" className={linkClass}>
          <Settings size={20} />
          Settings
        </NavLink>

      </nav>

    </aside>
  );
}

export default Sidebar;