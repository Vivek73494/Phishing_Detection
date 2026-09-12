import React from 'react';
import { Shield, CheckCircle2, Cpu } from 'lucide-react';

export default function Navbar({ modelOnline = true }) {
  return (
    <header className="header">
      <div className="logo-area">
        <div className="logo-icon-box">
          <Shield size={26} />
        </div>
        <div className="logo-text">
          <h1>
            CYBER<span className="highlight">GUARD</span>
          </h1>
          <p className="subtitle">AI-Powered Real-Time Phishing Detection Engine</p>
        </div>
      </div>
      <div className="header-badges">
        <span className={`badge ${modelOnline ? 'badge-success' : 'badge-danger'}`}>
          <CheckCircle2 size={14} />
          {modelOnline ? 'RF Model Active' : 'Model Offline'}
        </span>
        <span className="badge badge-info">
          <Cpu size={14} />
          50 ML Features
        </span>
      </div>
    </header>
  );
}
