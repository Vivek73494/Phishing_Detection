/**
 * API Configuration for CyberGuard Phishing Detection System
 *
 * Local Development: http://127.0.0.1:5000
 * Production (Render): https://phishing-detection-2qz4.onrender.com
 *
 * Automatically detects whether the app is running locally or deployed on Vercel,
 * while respecting any explicit VITE_API_BASE_URL environment variable.
 */

export const getApiBaseUrl = () => {
  const envUrl = import.meta.env.VITE_API_BASE_URL;

  // When running locally in browser (Vite dev server on localhost or run_app.py on 127.0.0.1)
  if (
    typeof window !== 'undefined' &&
    (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
  ) {
    if (envUrl && !envUrl.includes('onrender.com')) {
      return envUrl.trim().replace(/\/+$/, '');
    }
    return 'http://127.0.0.1:5000';
  }

  // Explicit Vite environment variable (from Vercel build settings or .env.production)
  if (envUrl && envUrl.trim() !== '') {
    return envUrl.trim().replace(/\/+$/, '');
  }

  // Production fallback (Render backend URL)
  return 'https://phishing-detection-2qz4.onrender.com';
};

export const API_BASE_URL = getApiBaseUrl();
