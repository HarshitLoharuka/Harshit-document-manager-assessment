

import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './LoginPage';
import FileVersions from './FileVersions';
import DashboardPage from './DashboardPage';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <Routes>
            <Route
              path="/"
              element={<LoginPage />}
            />

            <Route path="/file-versions" element={<FileVersions />} />
            <Route path="/dashboard"  element={<DashboardPage />}  />
          </Routes>
        </header>
      </div>
    </Router>
  );
}

export default App;