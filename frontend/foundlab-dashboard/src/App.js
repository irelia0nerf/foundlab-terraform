import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import CaseView from './components/CaseView';

function App() {
  return (
    <div className="App">
      <header>
        <h1>FoundLab Compliance Dashboard</h1>
      </header>
      <main>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/cases/:caseId" element={<CaseView />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;