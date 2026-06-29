import {
  Home,
  FolderOpen,
  Clock3,
  Settings,
  Brain,
} from "lucide-react";

function Sidebar() {
  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-700 flex flex-col p-6">

      <div className="flex items-center gap-3 mb-12">

        <Brain size={34} className="text-cyan-400"/>

        <div>

          <h1 className="text-2xl font-bold text-white">
            EchoMind
          </h1>

          <p className="text-slate-400 text-sm">
            AI Memory OS
            
            <br></br>
            v0.1 Alpha
          </p>

        </div>

      </div>

      <nav className="space-y-3">

        <button className="flex items-center gap-3 w-full rounded-xl bg-cyan-500/20 text-cyan-400 p-3">

          <Home size={20}/>

          Home

        </button>

        <button className="flex items-center gap-3 w-full rounded-xl hover:bg-slate-800 p-3">

          <FolderOpen size={20}/>

          Documents

        </button>

        <button className="flex items-center gap-3 w-full rounded-xl hover:bg-slate-800 p-3">

          <Clock3 size={20}/>

          Recent

        </button>

        <button className="flex items-center gap-3 w-full rounded-xl hover:bg-slate-800 p-3">

          <Settings size={20}/>

          Settings

        </button>

      </nav>

    </aside>
  );
}

export default Sidebar;