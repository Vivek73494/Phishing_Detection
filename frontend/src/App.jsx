import React, { useState, useEffect, useRef } from 'react';
import Navbar from './components/Navbar';
import ScannerForm from './components/ScannerForm';
import ScanningAnimation from './components/ScanningAnimation';
import VerdictCard from './components/VerdictCard';
import UrlComponents from './components/UrlComponents';
import NetworkMetadata from './components/NetworkMetadata';
import FeatureInspection from './components/FeatureInspection';
import Footer from './components/Footer';
import { API_BASE_URL } from './apiConfig';

export default function App() {
  const [modelOnline, setModelOnline] = useState(true);
  const [isScanning, setIsScanning] = useState(false);
  const [currentStep, setCurrentStep] = useState(1);
  const [progress, setProgress] = useState(10);
  const [targetUrl, setTargetUrl] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const stepTimerRef = useRef(null);

  // Health check on mount
  useEffect(() => {
    fetch(`${API_BASE_URL}/api/health`)
      .then((res) => res.json())
      .then((data) => {
        if (data && data.status === 'online' && data.model_loaded) {
          setModelOnline(true);
        }
      })
      .catch(() => {
        // Backend might not be running yet, but keep UI responsive
        setModelOnline(false);
      });
  }, []);

  const handleScan = async (urlToScan) => {
    setError(null);
    setResult(null);
    setTargetUrl(urlToScan);
    setIsScanning(true);
    setCurrentStep(1);
    setProgress(15);

    // Simulated animated progress phases while live API request processes
    if (stepTimerRef.current) clearInterval(stepTimerRef.current);
    let step = 1;
    stepTimerRef.current = setInterval(() => {
      step++;
      if (step <= 5) {
        setCurrentStep(step);
        setProgress(step * 18);
      }
    }, 450);

    try {
      const response = await fetch(`${API_BASE_URL}/api/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: urlToScan }),
      });

      const data = await response.json();

      if (stepTimerRef.current) clearInterval(stepTimerRef.current);
      setProgress(100);

      // Brief delay for user to see completed progress
      setTimeout(() => {
        setIsScanning(false);
        if (response.ok && data.success) {
          setResult(data);
          setModelOnline(true);
        } else {
          setError(data.error || 'Failed to scan the URL. Please verify the URL and try again.');
        }
      }, 350);
    } catch (err) {
      if (stepTimerRef.current) clearInterval(stepTimerRef.current);
      setIsScanning(false);
      setError('Unable to reach the backend security API. Please ensure the backend server (app.py) is running on port 5000.');
    }
  };

  const handleClearError = () => {
    setError(null);
  };

  return (
    <div className="app-container">
      <Navbar modelOnline={modelOnline} />

      <main style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
        <ScannerForm
          onScan={handleScan}
          isScanning={isScanning}
          error={error}
          onClearError={handleClearError}
        />

        {isScanning && (
          <ScanningAnimation
            targetUrl={targetUrl}
            currentStep={currentStep}
            progress={progress}
          />
        )}

        {!isScanning && result && (
          <div className="results-container">
            <VerdictCard result={result} />

            <div className="grid-2">
              <UrlComponents components={result.components} />
              <NetworkMetadata metadata={result.fetch_metadata} />
            </div>

            <FeatureInspection features={result.features} />
          </div>
        )}
      </main>

      <Footer />
    </div>
  );
}
