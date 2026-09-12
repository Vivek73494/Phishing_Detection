import React from 'react';
import { Shield, Loader2, CheckCircle2, CircleDot } from 'lucide-react';

const STEPS = [
  "1. Validating URL syntax & format",
  "2. Parsing scheme, domain, and component structure",
  "3. Extracting 22 Lexical URL features",
  "4. Fetching live webpage HTML & analyzing DOM behavior",
  "5. Performing Random Forest 50-vector inference"
];

export default function ScanningAnimation({ targetUrl, currentStep, progress }) {
  return (
    <section className="card scanning-card">
      <div className="cyber-spinner">
        <Shield size={28} color="#06b6d4" />
      </div>
      <h3>Performing Real-Time Security Analysis...</h3>
      <p className="target-preview">Target: {targetUrl}</p>

      <div className="progress-track">
        <div className="progress-fill" style={{ width: `${progress}%` }} />
      </div>

      <div className="steps-list">
        {STEPS.map((stepText, index) => {
          const stepNum = index + 1;
          const isCompleted = currentStep > stepNum;
          const isActive = currentStep === stepNum;

          return (
            <div
              key={index}
              className={`step-item ${isCompleted ? 'completed' : ''} ${isActive ? 'active' : ''}`}
            >
              {isCompleted ? (
                <CheckCircle2 size={16} color="#34d399" />
              ) : isActive ? (
                <Loader2 size={16} color="#38bdf8" className="animate-spin" style={{ animation: 'spin 1s linear infinite' }} />
              ) : (
                <CircleDot size={16} color="#64748b" />
              )}
              <span>{stepText}</span>
            </div>
          );
        })}
      </div>
    </section>
  );
}
