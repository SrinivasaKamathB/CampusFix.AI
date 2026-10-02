import React, { useState, useEffect } from 'react';
import { api } from '../services/api';

export default function MaintenanceBoard({ onNavigate }) {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadTasks = async () => {
    setLoading(true);
    try {
      const data = await api.getMaintenanceTasks();
      setTasks(data);
      setLoading(false);
    } catch (err) {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTasks();
  }, []);

  const handleUploadAfter = async (taskId) => {
    try {
      const res = await fetch(`http://localhost:8000/demo_assets/classroom_fan_fixed.svg`);
      const text = await res.text();
      const b64 = `data:image/svg+xml;base64,${btoa(text)}`;
      
      const uploadRes = await api.uploadAfterPhoto(
        taskId,
        b64,
        "Campus Maintenance Team",
        "Replaced damaged fan blade with balanced 3-blade unit."
      );

      alert(`After-Photo uploaded! AI Verification: ${uploadRes.verification_result.verification_status} (${Math.round(uploadRes.verification_result.resolution_confidence * 100)}% Conf)`);
      onNavigate('verification');
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="space-y-5">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-xl font-extrabold text-white">Technician Work Orders</h2>
          <p className="text-xs text-slate-400 mt-0.5">Tasks dispatched with photo evidence. Upload post-repair photo to trigger AI verification.</p>
        </div>
        <button onClick={loadTasks} className="px-3 py-1.5 bg-[#232F45] hover:bg-[#334155] text-xs font-semibold rounded-lg text-slate-200">
          🔄 Refresh
        </button>
      </div>

      {loading ? (
        <div className="text-center py-12 text-slate-500 text-xs">Loading tasks...</div>
      ) : (
        <div className="space-y-3">
          {tasks.map(task => (
            <div key={task.id} className="bg-[#151D2C] border border-[#232F45] hover:border-sky-500/40 p-4 rounded-xl flex justify-between items-center transition">
              <div className="flex items-center gap-4">
                <div className="w-16 h-16 rounded-lg bg-[#0B0F19] border border-[#232F45] overflow-hidden flex-shrink-0">
                  <img src={task.before_image || ''} alt="" className="w-full h-full object-contain" />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="px-2 py-0.5 bg-slate-800 text-slate-300 text-[10px] font-bold rounded">{task.id}</span>
                    <h4 className="text-sm font-bold text-white">{task.title}</h4>
                    <span className="px-2 py-0.5 bg-amber-500/20 text-amber-300 text-[10px] font-bold rounded">{task.priority}</span>
                  </div>
                  <div className="text-xs text-slate-400 mt-1">
                    📍 {task.location} &nbsp;|&nbsp; 🏢 {task.department} &nbsp;|&nbsp; 👍 {task.upvotes} reports merged
                  </div>
                </div>
              </div>

              <div className="flex gap-2">
                {task.status === 'Awaiting Verification' ? (
                  <button onClick={() => onNavigate('verification')} className="px-3 py-2 bg-[#232F45] hover:bg-[#334155] text-sky-400 font-bold text-xs rounded-lg">
                    🔍 View AI Diff
                  </button>
                ) : (
                  <button onClick={() => handleUploadAfter(task.id)} className="px-3.5 py-2 bg-sky-500 hover:bg-sky-400 text-slate-950 font-bold text-xs rounded-lg shadow">
                    📷 Upload After Photo
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
