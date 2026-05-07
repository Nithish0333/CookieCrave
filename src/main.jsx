import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css'
import './index.css'
import App from './App.jsx'

// Initialize analytics safely
try {
  import('./services/analyticsService').then(analytics => {
    console.log('Analytics service initialized:', analytics.default.getSessionInfo());
  }).catch(err => {
    console.warn('Analytics service failed to initialize:', err);
  });
} catch (err) {
  console.warn('Analytics service not available:', err);
}

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
