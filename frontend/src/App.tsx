import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Dashboard from './pages/Dashboard';
import PatientProfile from './pages/PatientProfile';
import DocumentUpload from './pages/DocumentUpload';
import ProviderSearch from './pages/ProviderSearch';
import InsuranceClaims from './pages/InsuranceClaims';
import './App.css';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Header />
        <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          <div className="px-4 py-6 sm:px-0">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/profile" element={<PatientProfile />} />
              <Route path="/documents" element={<DocumentUpload />} />
              <Route path="/providers" element={<ProviderSearch />} />
              <Route path="/insurance" element={<InsuranceClaims />} />
            </Routes>
          </div>
        </main>
      </div>
    </Router>
  );
}

export default App;
