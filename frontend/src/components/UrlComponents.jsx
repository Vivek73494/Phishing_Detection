import React from 'react';
import { Network } from 'lucide-react';

export default function UrlComponents({ components }) {
  if (!components) return null;

  const items = [
    { label: 'Scheme', value: components.Scheme || 'http' },
    { label: 'Domain', value: components.Domain || 'None', highlight: true },
    { label: 'Subdomain', value: components.Subdomain || 'None' },
    { label: 'Path', value: components.Path || '/' },
    { label: 'Query', value: components.Query || 'None' },
    { label: 'Fragment', value: components.Fragment || 'None' }
  ];

  return (
    <div className="card info-card">
      <div className="card-title">
        <Network size={18} color="#06b6d4" />
        Parsed URL Components
      </div>
      <div className="components-grid">
        {items.map((item, index) => (
          <div key={index} className="comp-tile">
            <span className="comp-label">{item.label}</span>
            <span className={`comp-val ${item.highlight ? 'highlight' : ''}`}>{item.value}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
