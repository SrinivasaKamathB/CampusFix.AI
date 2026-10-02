import React, { useState } from 'react';
import { api } from '../services/api';

export default function StudentReporter({ onNavigate }) {
  const [mode, setMode] = useState('single');
  const [location, setLocation] = useState('Block B / Room 204');
  const [imagePreview, setImagePreview] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [duplicateWarning, setDuplicateWarning] = useState(null);

  const loadPreset = async (presetType) => {
    let filename = 'classroom_fan_broken.svg';
    let loc = 'Block B / Room 204';
    if (presetType === 'room') {
      filename = 'classroom_wide_scan.svg';
      setMode('room');
    } else if (presetType === 'leak') {
      filename = 'washroom_leak.svg';
      loc = 'Block C / 2nd Fl Washroom';
      setMode('single');
    } else {
      setMode('single');
    }
    setLocation(loc);

    try {
      const res = await fetch(`http://localhost:8000/demo_assets/${filename}`);
      const text = await res.text();
      const b64 = `data:image/svg+xml;base64,${btoa(text)}`;
      setImagePreview(b64);
      runAnalysis(b64, loc, presetType === 'room');
    } catch (err) {
      console.error(err);
    }
  };

  const runAnalysis = async (img, loc, isRoom) => {
    setIsAnalyzing(true);
    setAnalysisResult(null);
    setDuplicateWarning(null);

    try {
      const res = await api.analyzeImage(img, loc, isRoom);
      setIsAnalyzing(false);
      setAnalysisResult(res);

      if (res.mode === 'single_issue') {
        const dupRes = await api.checkDuplicates(loc, res.data.category, res.data.object);
        if (dupRes.is_duplicate) {
          setDuplicateWarning(dupRes.matched_incident);
        }
      }
    } catch (err) {
      setIsAnalyzing(false);
    }
  };

  const handleUpvote = async () => {
    if (!duplicateWarning) return;
    await api.upvoteIncident(duplicateWarning.id);
    alert(`Merged into Ticket ${duplicateWarning.id}! You are now tracking this fix.`);
    onNavigate('maintenance');
  };

  return (
    <div className="space-y-6">
      <div className="bg-[#151D2C] border-l-4 border-sky-400 p-5 rounded-xl border border-[#232F45]">
        <h2 className="text-xl font-extrabold text-white">"Don't fill a complaint form. Show the problem."</h2>
        <p className="text-xs text-slate-400 mt-1">Single photo snap or whole-room multi-defect scan. Autonomous classification, deduplication, and department routing.</p>
      </div>

      <div className="flex gap-3">
        <button
          onClick={() => setMode('single')}
          className={`px-4 py-2 text-xs font-bold rounded-lg border ${mode === 'single' ? 'bg-sky-500 text-slate-950 border-sky-400' : 'bg-[#151D2C] text-slate-300 border-[#2B3A54]'}`}
        >
          📷 Single Defect Mode
        </button>
        <button
          onClick={() => setMode('room')}
          className={`px-4 py-2 text-xs font-bold rounded-lg border ${mode === 'room' ? 'bg-sky-500 text-slate-950 border-sky-400' : 'bg-[#151D2C] text-slate-300 border-[#2B3A54]'}`}
        >
          🔍 Room Scan Mode (Multi-Defect Audit)
        </button>
      </div>

      {/* Preset Chips */}
      <div>
        <div className="text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-2">⚡ 1-Click Demo Scenarios:</div>
        <div className="flex flex-wrap gap-2.5">
          <button onClick={() => loadPreset('fan')} className="px-3 py-2 bg-[#1B2436] hover:bg-sky-500/10 border border-[#2B3A54] hover:border-sky-400 text-slate-200 text-xs rounded-lg flex items-center gap-2">
            🌪️ <strong>Room 204: Broken Fan</strong> (Triggers Auto-Routing & Duplicate Check)
          </button>
          <button onClick={() => loadPreset('room')} className="px-3 py-2 bg-[#1B2436] hover:bg-sky-500/10 border border-[#2B3A54] hover:border-sky-400 text-slate-200 text-xs rounded-lg flex items-center gap-2">
            🏫 <strong>Room 204: Wide Scan</strong> (Detects 3 Defects in 1 Pass)
          </button>
          <button onClick={() => loadPreset('leak')} className="px-3 py-2 bg-[#1B2436] hover:bg-sky-500/10 border border-[#2B3A54] hover:border-sky-400 text-slate-200 text-xs rounded-lg flex items-center gap-2">
            🚰 <strong>Block C: Water Leak</strong> (Plumbing P1 Hazard)
          </button>
        </div>
      </div>

      {/* Duplicate Warning Prompt */}
      {duplicateWarning && (
        <div className="bg-amber-500/10 border border-amber-500/30 p-4 rounded-xl flex justify-between items-center">
          <div>
            <div className="text-amber-400 font-bold text-sm flex items-center gap-1.5">
              ⚠️ Possible Duplicate Detected! (Ticket #{duplicateWarning.id})
            </div>
            <div className="text-xs text-slate-300 mt-1">
              A matching report already exists in {duplicateWarning.location}.
            </div>
          </div>
          <button onClick={handleUpvote} className="px-4 py-2 bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs rounded-lg shadow">
            👍 Upvote & Track (+1)
          </button>
        </div>
      )}

      {/* Grid: Preview & Results */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-[#151D2C] border border-[#232F45] rounded-xl p-5">
          <h3 className="text-sm font-bold text-white mb-3">1. Captured Evidence</h3>
          <div className="h-64 bg-[#0F172A] border-2 border-dashed border-[#2B3A54] rounded-xl flex items-center justify-center overflow-hidden">
            {imagePreview ? (
              <img src={imagePreview} alt="Preview" className="w-full h-full object-contain" />
            ) : (
              <span className="text-xs text-slate-500">Select a Demo Scenario or Upload Photo</span>
            )}
          </div>
          <input
            type="text"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            className="w-full mt-3 bg-[#0F172A] border border-[#2B3A54] rounded-lg px-3 py-2 text-xs text-white"
            placeholder="Room Location"
          />
        </div>

        <div className="bg-[#151D2C] border border-[#232F45] rounded-xl p-5">
          <h3 className="text-sm font-bold text-white mb-3">2. AI Vision Understanding</h3>
          {isAnalyzing && (
            <div className="text-center py-20 text-sky-400 text-xs font-bold animate-pulse">
              Multimodal Vision AI Analyzing Scene...
            </div>
          )}

          {!isAnalyzing && !analysisResult && (
            <div className="text-center py-20 text-slate-500 text-xs">
              Load a scenario to run visual defect detection.
            </div>
          )}

          {analysisResult && analysisResult.mode === 'single_issue' && (
            <div className="space-y-4">
              <div className="bg-[#0E1626] border border-[#232F45] p-4 rounded-xl">
                <div className="flex justify-between items-start">
                  <div>
                    <h4 className="font-bold text-white text-base">{analysisResult.data.object}</h4>
                    <p className="text-xs text-rose-400 mt-0.5">{analysisResult.data.defect}</p>
                  </div>
                  <span className="px-2 py-0.5 bg-rose-500/20 text-rose-300 text-[10px] font-bold rounded">
                    {analysisResult.data.priority}
                  </span>
                </div>
                <p className="text-xs text-slate-300 mt-2">{analysisResult.data.summary}</p>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div className="bg-[#0F172A] p-3 rounded-lg border border-[#232F45]">
                  <div className="text-[10px] text-slate-400 uppercase font-semibold">Department</div>
                  <div className="text-xs font-bold text-sky-400 mt-0.5">{analysisResult.data.department}</div>
                </div>
                <div className="bg-[#0F172A] p-3 rounded-lg border border-[#232F45]">
                  <div className="text-[10px] text-slate-400 uppercase font-semibold">Confidence</div>
                  <div className="text-xs font-bold text-emerald-400 mt-0.5">{Math.round(analysisResult.data.confidence * 100)}%</div>
                </div>
              </div>

              <button
                onClick={() => {
                  alert("Work order dispatched to " + analysisResult.data.department);
                  onNavigate('maintenance');
                }}
                className="w-full py-2.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs rounded-xl shadow"
              >
                🚀 Dispatch Work Order
              </button>
            </div>
          )}

          {analysisResult && analysisResult.mode === 'room_scan' && (
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-xs font-bold text-sky-400">{analysisResult.data.total_issues_detected} Defects Detected Simultaneously</span>
                <span className="px-2 py-0.5 bg-indigo-500/20 text-indigo-300 text-[10px] font-bold rounded">Room Scan</span>
              </div>
              {analysisResult.data.candidate_issues.map(iss => (
                <div key={iss.id} className="bg-[#0F172A] border border-[#232F45] p-3 rounded-lg flex justify-between items-center text-xs">
                  <div>
                    <div className="font-bold text-white">{iss.object}</div>
                    <div className="text-[11px] text-slate-400">{iss.defect} ({iss.bounding_area})</div>
                  </div>
                  <span className="px-2 py-0.5 bg-slate-800 text-slate-300 text-[10px] rounded font-bold">{iss.department}</span>
                </div>
              ))}
              <button
                onClick={() => {
                  alert("Batch created 3 work orders!");
                  onNavigate('maintenance');
                }}
                className="w-full py-2.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs rounded-xl shadow mt-2"
              >
                ✅ Confirm & Dispatch All 3 Tasks
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
