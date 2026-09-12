import React from 'react';
import { Server, Activity, Type, CornerUpRight, CheckCircle, AlertTriangle } from 'lucide-react';

export default function NetworkMetadata({ metadata }) {
  if (!metadata) return null;

  const isSuccess = metadata.fetch_success;

  return (
    <div className="card info-card">
      <div className="card-title">
        <Server size={18} color="#06b6d4" />
        Live HTTP Fetch & DOM Info
      </div>
      <div className="meta-list">
        <div className="meta-row">
          <span className="meta-label">
            <Activity size={15} /> HTTP Status:
          </span>
          <span className={`badge ${isSuccess ? 'badge-success' : 'badge-danger'}`}>
            {metadata.status_code ? `HTTP ${metadata.status_code}` : 'No Response'}
          </span>
        </div>

        <div className="meta-row">
          <span className="meta-label">
            <Type size={15} /> Page Title:
          </span>
          <span className="meta-value text-truncate" title={metadata.page_title || 'N/A'}>
            {metadata.page_title || 'N/A'}
          </span>
        </div>

        <div className="meta-row">
          <span className="meta-label">
            <CornerUpRight size={15} /> Redirect Count:
          </span>
          <span className="meta-value">{metadata.redirect_count || 0}</span>
        </div>

        <div className="meta-row">
          <span className="meta-label">
            <CheckCircle size={15} /> Fetch Status:
          </span>
          <span className={`badge ${isSuccess ? 'badge-success' : 'badge-danger'}`}>
            {isSuccess ? 'Success' : 'Failed / Network Error'}
          </span>
        </div>

        {metadata.error_message && (
          <div className="meta-row">
            <span className="meta-label text-warning">
              <AlertTriangle size={15} /> Network Note:
            </span>
            <span className="meta-value" style={{ color: '#f59e0b' }}>
              {metadata.error_message}
            </span>
          </div>
        )}
      </div>
    </div>
  );
}
