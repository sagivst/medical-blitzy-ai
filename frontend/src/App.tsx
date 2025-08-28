import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Header from './components/Header';
import Dashboard from './pages/Dashboard';
import PatientProfile from './pages/PatientProfile';
import DocumentUpload from './pages/DocumentUpload';
import ProviderSearch from './pages/ProviderSearch';
import InsuranceClaims from './pages/InsuranceClaims';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Header />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/profile" element={<PatientProfile />} />
            <Route path="/documents" element={<DocumentUpload />} />
            <Route path="/providers" element={<ProviderSearch />} />
            <Route path="/insurance" element={<InsuranceClaims />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
