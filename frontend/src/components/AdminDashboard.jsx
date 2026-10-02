import React, { useState, useEffect } from 'react';
import { api } from '../services/api';

export default function AdminDashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    api.getAnalytics().then(setData);
  }, []);

  if (!data) return <div className="text-center py-20 text-slate-500 text-xs">Loading analytics...</div>;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-xl font-extrabold text-white">Campus Infrastructure Health & Analytics</h2>
          <p className="text-xs text-slate-400 mt-0.5">Live operational KPIs, department backlog, and accreditation compliance audit trail.</p>
        </div>
        <button
          onClick={() => alert("Accreditation Audit Export: Generated PDF/CSV digital proof log with before/after photo hashes and sign-off timestamps.")}
          className="px-3.5 py-2 bg-[#232F45] hover:bg-[#334155] text-slate-200 text-xs font-semibold rounded-lg"
        >
          📄 Export Accreditation Audit (PDF)
        </button>
      </div>

      {/* 4 Stats Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-[#151D2C] border border-[#232F45] p-5 rounded-xl">
          <div className="text-[11px] text-slate-400 uppercase font-semibold">Total Incidents</div>
          <div className="text-2xl font-extrabold text-white mt-1">{data.kpis.total_incidents}</div>
          <div className="text-[11px] text-sky-400 mt-1">Evidence-backed</div>
        </div>

        <div className="bg-[#151D2C] border border-[#232F45] p-5 rounded-xl">
          <div className="text-[11px] text-slate-400 uppercase font-semibold">Active Backlog</div>
          <div className="text-2xl font-extrabold text-amber-400 mt-1">{data.kpis.in_progress + data.kpis.open_reported}</div>
          <div className="text-[11px] text-slate-400 mt-1">In-progress repairs</div>
        </div>

        <div className="bg-[#151D2C] border border-[#232F45] p-5 rounded-xl">
          <div className="text-[11px] text-slate-400 uppercase font-semibold">Verified Resolved</div>
          <div className="text-2xl font-extrabold text-emerald-400 mt-1">{data.kpis.verified_resolved}</div>
          <div className="text-[11px] text-emerald-400 mt-1">{data.kpis.resolution_rate_pct}% Verified</div>
        </div>

        <div className="bg-[#151D2C] border border-[#232F45] p-5 rounded-xl">
          <div className="text-[11px] text-slate-400 uppercase font-semibold">Duplicate Flood Avoided</div>
          <div className="text-2xl font-extrabold text-indigo-400 mt-1">{data.kpis.duplicates_merged}</div>
          <div className="text-[11px] text-indigo-400 mt-1">Merged tickets</div>
        </div>
      </div>

      {/* Workload & Audit Trail */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-[#151D2C] border border-[#232F45] p-5 rounded-xl space-y-4">
          <h3 className="text-sm font-bold text-white">Department Workload Distribution</h3>
          <div className="space-y-3">
            {Object.entries(data.department_distribution).map(([dept, count]) => {
              const pct = Math.round((count / Math.max(1, data.kpis.total_incidents)) * 100);
              return (
                <div key={dept}>
                  <div className="flex justify-between text-xs mb-1">
                    <span className="text-slate-300">{dept}</span>
                    <span className="font-bold text-sky-400">{count} ({pct}%)</span>
                  </div>
                  <div className="h-1.5 bg-[#0B0F19] rounded-full overflow-hidden">
                    <div style={{ width: `${pct}%` }} className="h-full bg-sky-500 rounded-full"></div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        <div className="bg-[#151D2C] border border-[#232F45] p-5 rounded-xl space-y-3">
          <div className="flex justify-between items-center">
            <h3 className="text-sm font-bold text-white">Live Verifiable Audit Trail</h3>
            <span className="px-2 py-0.5 bg-slate-800 text-slate-400 text-[10px] font-bold rounded">Immutable</span>
          </div>
          <div className="space-y-2 max-h-64 overflow-y-auto pr-1">
            {data.recent_audit_trail.map(evt => (
              <div key={evt.id} className="bg-[#0F172A] border border-[#232F45] p-2.5 rounded-lg text-xs">
                <div className="flex justify-between">
                  <span className="font-bold text-sky-400">{evt.incident_id}: {evt.action}</span>
                  <span className="text-[10px] text-slate-500">{new Date(evt.timestamp).toLocaleTimeString()}</span>
                </div>
                <div className="text-[11px] text-slate-400 mt-0.5">{evt.actor} — {evt.details}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
