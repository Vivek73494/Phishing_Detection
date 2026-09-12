import React, { useState } from 'react';
import { ListChecks, Database, Code, Search } from 'lucide-react';
import { FEATURE_DESCRIPTIONS } from '../constants/featureDescriptions';

export default function FeatureInspection({ features }) {
  const [activeTab, setActiveTab] = useState('url');
  const [searchFilter, setSearchFilter] = useState('');

  if (!features) return null;

  const urlFeatures = features.url_features || {};
  const htmlFeatures = features.html_features || {};
  const all50 = features.all_50_features || {};
  const expectedCols = features.expected_columns || Object.keys(all50);

  const filterFeatures = (featureObj) => {
    return Object.entries(featureObj).filter(([name, val]) => {
      const desc = FEATURE_DESCRIPTIONS[name] || '';
      const term = searchFilter.toLowerCase();
      return name.toLowerCase().includes(term) || desc.toLowerCase().includes(term);
    });
  };

  return (
    <div className="card feature-card">
      <div className="feature-card-header">
        <div>
          <h3>
            <ListChecks size={20} color="#06b6d4" />
            Extracted Feature Inspection (50 ML Features)
          </h3>
          <p>Detailed view of the 22 URL & 28 HTML features extracted live for Random Forest classification</p>
        </div>

        <div className="tab-buttons">
          <button
            type="button"
            className={`tab-btn ${activeTab === 'url' ? 'active' : ''}`}
            onClick={() => setActiveTab('url')}
          >
            URL Features (22)
          </button>
          <button
            type="button"
            className={`tab-btn ${activeTab === 'html' ? 'active' : ''}`}
            onClick={() => setActiveTab('html')}
          >
            HTML Features (28)
          </button>
          <button
            type="button"
            className={`tab-btn ${activeTab === 'vector' ? 'active' : ''}`}
            onClick={() => setActiveTab('vector')}
          >
            Full Model Vector (50)
          </button>
        </div>
      </div>

      {activeTab !== 'vector' && (
        <div style={{ marginBottom: 16, display: 'flex', alignItems: 'center', background: 'rgba(0,0,0,0.25)', padding: '6px 12px', borderRadius: 8, border: '1px solid rgba(255,255,255,0.06)' }}>
          <Search size={16} color="#64748b" style={{ marginRight: 8 }} />
          <input
            type="text"
            placeholder="Filter features by name or description..."
            value={searchFilter}
            onChange={(e) => setSearchFilter(e.target.value)}
            style={{ background: 'transparent', border: 'none', outline: 'none', color: '#f8fafc', fontSize: '0.85rem', width: '100%' }}
          />
        </div>
      )}

      {/* Tab 1: 22 URL Features */}
      {activeTab === 'url' && (
        <div className="table-responsive">
          <table className="feature-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Feature Name</th>
                <th>Extracted Value</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              {filterFeatures(urlFeatures).map(([name, val], idx) => (
                <tr key={name}>
                  <td>{idx + 1}</td>
                  <td>{name}</td>
                  <td>{String(val)}</td>
                  <td>{FEATURE_DESCRIPTIONS[name] || 'Extracted URL lexical metric.'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Tab 2: 28 HTML Features */}
      {activeTab === 'html' && (
        <div className="table-responsive">
          <table className="feature-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Feature Name</th>
                <th>Extracted Value</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              {filterFeatures(htmlFeatures).map(([name, val], idx) => (
                <tr key={name}>
                  <td>{idx + 1}</td>
                  <td>{name}</td>
                  <td>{String(val)}</td>
                  <td>{FEATURE_DESCRIPTIONS[name] || 'Extracted DOM / HTML metric.'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Tab 3: Full 50-Feature Vector */}
      {activeTab === 'vector' && (
        <div>
          <p style={{ fontSize: '0.85rem', color: '#94a3b8', display: 'flex', alignItems: 'center', gap: 6 }}>
            <Database size={16} color="#06b6d4" />
            Exact feature vector passed into Random Forest classifier in dataset column order:
          </p>
          <div className="vector-grid">
            {expectedCols.map((colName, idx) => {
              const val = all50[colName] !== undefined ? all50[colName] : 0;
              return (
                <div key={colName} className="vector-chip">
                  <span className="chip-name" title={colName}>
                    [{idx + 1}] {colName}:
                  </span>
                  <span className="chip-val">{String(val)}</span>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
