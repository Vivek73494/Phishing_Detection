import React from 'react';
import { ShieldCheck, ShieldAlert, Link2, GitFork, Info } from 'lucide-react';

export default function VerdictCard({ result }) {
  if (!result) return null;

  const isPhishing = result.is_phishing;
  const legitProb = result.probabilities?.legitimate ?? (isPhishing ? 100 - result.confidence_score : result.confidence_score);
  const phishProb = result.probabilities?.phishing ?? (isPhishing ? result.confidence_score : 100 - result.confidence_score);
  const treeVotes = result.tree_votes;
  const winningVotes = isPhishing ? treeVotes?.phishing : treeVotes?.legitimate;

  return (
    <div className={`card verdict-card ${isPhishing ? 'phishing' : 'legitimate'}`}>
      <div className="verdict-header">
        <div className="verdict-badge">
          {isPhishing ? (
            <ShieldAlert size={28} />
          ) : (
            <ShieldCheck size={28} />
          )}
          <span>{isPhishing ? 'PHISHING WEBSITE DETECTED' : 'LEGITIMATE WEBSITE'}</span>
        </div>
        <div className="confidence-box">
          <span className="confidence-label">Model Confidence</span>
          <span className="confidence-value">{result.confidence_score.toFixed(2)}%</span>
          {treeVotes && (
            <span className="confidence-subtext">
              <GitFork size={13} />
              {winningVotes} / {treeVotes.total_trees} Trees Consensus
            </span>
          )}
        </div>
      </div>

      <div className="verdict-url-display">
        <Link2 size={18} color="#06b6d4" />
        <span>{result.url}</span>
      </div>

      {/* Probability Split Container */}
      <div className="probability-container">
        <div className="prob-labels">
          <span className="prob-text phish">
            Phishing Probability: <strong>{phishProb.toFixed(2)}%</strong>
          </span>
          <span className="prob-text legit">
            Legitimate Probability: <strong>{legitProb.toFixed(2)}%</strong>
          </span>
        </div>
        <div className="prob-track">
          <div className="prob-fill phish" style={{ width: `${phishProb}%` }} />
          <div className="prob-fill legit" style={{ width: `${legitProb}%` }} />
        </div>
        <p className="prob-note">
          <Info size={13} style={{ display: 'inline', verticalAlign: 'middle', marginRight: 4 }} />
          Probability represents the exact ratio of decision trees in the 50-tree Random Forest ensemble voting for each class based on the 50 extracted URL & DOM features.
        </p>
      </div>
    </div>
  );
}
