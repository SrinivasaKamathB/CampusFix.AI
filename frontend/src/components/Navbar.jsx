import React from 'react';

export default function Navbar({ activeTab, setActiveTab }) {
  return (
    <header className="bg-[#0E1626] border-b border-[#232F45] px-6 py-3.5 flex justify-between items-center sticky top-0 z-50">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-sky-500 via-blue-600 to-indigo-600 flex items-center justify-center text-white font-extrabold text-base tracking-tight shadow-lg shadow-sky-500/25 flex-shrink-0">
          CF
        </div>
        <div>
          <div className="text-white font-extrabold text-lg tracking-tight flex items-center gap-2">
            CampusFix <span className="bg-sky-500/15 text-sky-400 border border-sky-500/35 rounded-full px-2 py-0.5 text-xs font-bold">AI</span>
          </div>
          <div className="text-xs text-slate-400 font-medium">Visual Campus Maintenance & Resolution Intelligence</div>
        </div>
      </div>

      <nav className="flex bg-[#131C2E] border border-[#232F45] rounded-xl p-1 gap-1">
        <button
          onClick={() => setActiveTab('student')}
          className={`px-4 py-2 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${
            activeTab === 'student' ? 'bg-sky-500 text-slate-950 shadow-md' : 'text-slate-400 hover:text-white'
          }`}
        >
          📸 Student Reporter
        </button>
        <button
          onClick={() => setActiveTab('maintenance')}
          className={`px-4 py-2 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${
            activeTab === 'maintenance' ? 'bg-sky-500 text-slate-950 shadow-md' : 'text-slate-400 hover:text-white'
          }`}
        >
          🛠️ Maintenance Queue
        </button>
        <button
          onClick={() => setActiveTab('verification')}
          className={`px-4 py-2 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${
            activeTab === 'verification' ? 'bg-sky-500 text-slate-950 shadow-md' : 'text-slate-400 hover:text-white'
          }`}
        >
          🔍 AI Verification Hub
        </button>
        <button
          onClick={() => setActiveTab('admin')}
          className={`px-4 py-2 rounded-lg text-xs font-bold transition flex items-center gap-1.5 ${
            activeTab === 'admin' ? 'bg-sky-500 text-slate-950 shadow-md' : 'text-slate-400 hover:text-white'
          }`}
        >
          📊 Admin Dashboard
        </button>
      </nav>
    </header>
  );
}
