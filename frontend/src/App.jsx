import React, { useState } from 'react';
import Navbar from './components/Navbar';
import StudentReporter from './components/StudentReporter';
import MaintenanceBoard from './components/MaintenanceBoard';
import VerificationView from './components/VerificationView';
import AdminDashboard from './components/AdminDashboard';

export default function App() {
  const [activeTab, setActiveTab] = useState('student');

  return (
    <div className="min-h-screen bg-[#0B0F19] text-slate-100 flex flex-col font-sans">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <main className="flex-1 max-w-7xl w-full mx-auto p-6">
        {activeTab === 'student' && <StudentReporter onNavigate={setActiveTab} />}
        {activeTab === 'maintenance' && <MaintenanceBoard onNavigate={setActiveTab} />}
        {activeTab === 'verification' && <VerificationView onNavigate={setActiveTab} />}
        {activeTab === 'admin' && <AdminDashboard />}
      </main>
    </div>
  );
}
