import React, { useState } from 'react';
import { Globe, Search, ShieldAlert, AlertCircle, X } from 'lucide-react';

export default function ScannerForm({ onScan, isScanning, error, onClearError }) {
  const [url, setUrl] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (url.trim()) {
      onScan(url.trim());
    }
  };

  return (
    <section className="card scanner-card">
      <div className="scanner-header">
        <h2>
          <Search size={20} className="text-cyan" />
          Analyze Website URL
        </h2>
        <p>Enter any URL to extract real-time URL & HTML features and classify with Random Forest</p>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <div className="input-icon">
            <Globe size={20} />
          </div>
          <input
            type="text"
            className="url-input"
            value={url}
            onChange={(e) => {
              setUrl(e.target.value);
              if (error) onClearError();
            }}
            placeholder="Enter website URL to scan..."
            required
            autoComplete="off"
            disabled={isScanning}
          />
          <button type="submit" className="btn-scan" disabled={isScanning || !url.trim()}>
            <ShieldAlert size={18} />
            {isScanning ? 'Scanning...' : 'Scan URL'}
          </button>
        </div>
      </form>

      {error && (
        <div className="alert alert-danger">
          <AlertCircle size={20} className="alert-icon" />
          <div className="alert-content" style={{ flex: 1 }}>
            <h4>Scan Error</h4>
            <p>{error}</p>
          </div>
          <button
            type="button"
            onClick={onClearError}
            style={{ background: 'none', border: 'none', color: '#f87171', cursor: 'pointer' }}
          >
            <X size={18} />
          </button>
        </div>
      )}
    </section>
  );
}
