import React, { useState } from 'react';
import './App.css';

function App() {
  const [prompt, setPrompt] = useState('');
  const [expected, setExpected] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const runTest = async () => {
    setResult(null);
    setLoading(true);

    try {
    const res = await fetch('http://localhost:5000/run_test', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: 'Manual UI Test',
        prompt: prompt,
        assertion: {
          type: 'includes',
          expected: expected,
          source: 'result'
        }
      })
    });
    const text = await res.text(); // First get raw response
    let data;

    try {
      data = JSON.parse(text); // Then safely parse
    } catch (jsonError) {
      throw new Error(`Invalid JSON response from backend: ${text}`);
    }
    setResult(data);
  } catch (error) {
    setResult({ error: 'Failed to run test: ' + error.message });
  } finally {
    setLoading(false);
  }
  };

  return (
    <div className="App">
      <h2>Prompt Runner UI</h2>
      <textarea
        placeholder="Enter prompt..."
        value={prompt}
        onChange={e => setPrompt(e.target.value)}
        rows="4" cols="50"
      />
      <br />
      <input
        type="text"
        placeholder="Expected Assertion Value"
        value={expected}
        onChange={e => setExpected(e.target.value)}
        rows="4" cols="50"
      />
      <br /><br />
      <button onClick={runTest} disabled={loading}>
        {loading ? 'Running Test...' : 'Run Test'}
      </button>
      {loading && (
        <div>
          <p>Running test, please wait...</p>
        </div>
      )}

{result && !loading && (
        <div>
          <h3>Test Result</h3>
          <table style={{ 
            border: '1px solid #ccc', 
            borderCollapse: 'collapse', 
            width: '100%', 
            marginTop: '20px' 
          }}>
            <thead>
              <tr style={{ backgroundColor: '#f5f5f5' }}>
                <th style={{ border: '1px solid #ccc', padding: '8px', textAlign: 'left' }}>
                  Property
                </th>
                <th style={{ border: '1px solid #ccc', padding: '8px', textAlign: 'left' }}>
                  Value
                </th>
              </tr>
            </thead>
            <tbody>
              <tr style={{ 
                backgroundColor: result.error ? '#ffebee' : (result.passed ? '#e8f5e8' : '#fff3cd'),
                color: result.error ? '#c62828' : (result.passed ? '#2e7d32' : '#856404')
              }}>
                <td style={{ border: '1px solid #ccc', padding: '8px', fontWeight: 'bold' }}>
                  Status
                </td>
                <td style={{ border: '1px solid #ccc', padding: '8px' }}>
                  {result.error ? 'ERROR' : (result.passed ? 'PASS' : 'FAIL')}
                </td>
              </tr>
              {result.name && (
                <tr>
                  <td style={{ border: '1px solid #ccc', padding: '8px', fontWeight: 'bold' }}>
                    Test Name
                  </td>
                  <td style={{ border: '1px solid #ccc', padding: '8px' }}>
                    {result.name}
                  </td>
                </tr>
              )}
              {result.prompt && (
                <tr>
                  <td style={{ border: '1px solid #ccc', padding: '8px', fontWeight: 'bold' }}>
                    Prompt
                  </td>
                  <td style={{ border: '1px solid #ccc', padding: '8px' }}>
                    {result.prompt}
                  </td>
                </tr>
              )}
              {result.result && (
                <tr>
                  <td style={{ border: '1px solid #ccc', padding: '8px', fontWeight: 'bold' }}>
                    Result
                  </td>
                  <td style={{ border: '1px solid #ccc', padding: '8px' }}>
                    {result.result}
                  </td>
                </tr>
              )}
              {result.expected && (
                <tr>
                  <td style={{ border: '1px solid #ccc', padding: '8px', fontWeight: 'bold' }}>
                    Expected
                  </td>
                  <td style={{ border: '1px solid #ccc', padding: '8px' }}>
                    {result.expected}
                  </td>
                </tr>
              )}
              {result.error && (
                <tr style={{ backgroundColor: '#ffebee', color: '#c62828' }}>
                  <td style={{ border: '1px solid #ccc', padding: '8px', fontWeight: 'bold' }}>
                    Error
                  </td>
                  <td style={{ border: '1px solid #ccc', padding: '8px' }}>
                    {result.error}
                  </td>
                </tr>
              )}
              {result.message && (
                <tr>
                  <td style={{ border: '1px solid #ccc', padding: '8px', fontWeight: 'bold' }}>
                    Message
                  </td>
                  <td style={{ border: '1px solid #ccc', padding: '8px' }}>
                    {result.message}
                  </td>
                </tr>
              )}
              {result.duration && (
                <tr>
                  <td style={{ border: '1px solid #ccc', padding: '8px', fontWeight: 'bold' }}>
                    Duration
                  </td>
                  <td style={{ border: '1px solid #ccc', padding: '8px' }}>
                    {result.duration}ms
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default App;
