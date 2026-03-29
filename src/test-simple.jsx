import React from 'react';
import { createRoot } from 'react-dom/client';

function TestApp() {
  return (
    <div style={{ padding: '20px', textAlign: 'center' }}>
      <h1>React is Working!</h1>
      <p>CookieCrave Frontend Test</p>
    </div>
  );
}

const root = createRoot(document.getElementById('root'));
root.render(<TestApp />);
