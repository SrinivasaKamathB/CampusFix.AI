const API_BASE = "http://localhost:8000";

export const api = {
  analyzeImage: async (imageData, locationHint = "", isRoomScan = false) => {
    const res = await fetch(`${API_BASE}/api/analyze-image`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image_data: imageData, location_hint: locationHint, is_room_scan: isRoomScan })
    });
    return res.json();
  },

  checkDuplicates: async (location, category, objectName) => {
    const res = await fetch(`${API_BASE}/api/check-duplicates`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ location, category, object_name: objectName })
    });
    return res.json();
  },

  createIncident: async (incidentData) => {
    const res = await fetch(`${API_BASE}/api/incidents`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(incidentData)
    });
    return res.json();
  },

  createBatchIncidents: async (location, beforeImage, issues) => {
    const res = await fetch(`${API_BASE}/api/incidents/batch`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ location, before_image: beforeImage, issues })
    });
    return res.json();
  },

  listIncidents: async (status = "All") => {
    const url = status === "All" ? `${API_BASE}/api/incidents` : `${API_BASE}/api/incidents?status=${status}`;
    const res = await fetch(url);
    return res.json();
  },

  getIncident: async (id) => {
    const res = await fetch(`${API_BASE}/api/incidents/${id}`);
    return res.json();
  },

  upvoteIncident: async (id) => {
    const res = await fetch(`${API_BASE}/api/incidents/${id}/upvote`, { method: "POST" });
    return res.json();
  },

  getMaintenanceTasks: async () => {
    const res = await fetch(`${API_BASE}/api/maintenance/tasks`);
    return res.json();
  },

  uploadAfterPhoto: async (incidentId, afterImage, technicianName, notes) => {
    const res = await fetch(`${API_BASE}/api/maintenance/upload-after-photo`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        incident_id: incidentId,
        after_image: afterImage,
        technician_name: technicianName,
        repair_notes: notes
      })
    });
    return res.json();
  },

  getPendingVerifications: async () => {
    const res = await fetch(`${API_BASE}/api/verification/pending`);
    return res.json();
  },

  approveResolution: async (incidentId, supervisorName, notes) => {
    const res = await fetch(`${API_BASE}/api/verification/approve`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        incident_id: incidentId,
        supervisor_name: supervisorName,
        approval_notes: notes
      })
    });
    return res.json();
  },

  getAnalytics: async () => {
    const res = await fetch(`${API_BASE}/api/analytics`);
    return res.json();
  }
};
