import React, { useState } from 'react';

function App() {
  const [token, setToken] = useState(null);
  const [output, setOutput] = useState(null);

  const login = async () => {
    const response = await fetch('http://localhost:8000/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        username: 'admin',
        password: 'secret',
      })
    });
    const data = await response.json();
    setToken(data.access_token);
  };

  const runPlugin = async (formData) => {
    const response = await fetch('http://localhost:8000/run-plugin', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    });
    const data = await response.json();
    setOutput(data);
  };

  return (
    <div className="App">
      <h1>Run Data Pipeline</h1>
      <button onClick={login}>Login</button>
      <form onSubmit={e => {
        e.preventDefault();
        const formData = new FormData(e.target);
        runPlugin(formData);
      }}>
        <select name="plugin_type">
          <option value="csv">CSV to Excel</option>
          <option value="github">GitHub Repo</option>
        </select>
        <input type="text" name="repo_url" placeholder="GitHub repo URL" defaultValue="https://github.com/BejaminNaibei/dataset" />
        <input type="file" name="file" />
        <button type="submit" disabled={!token}>Run Plugin</button>
      </form>
      {output?.download_url && (
        <a href={`http://localhost:8000${output.download_url}`} download>
          Download Result
        </a>
      )}
    </div>
  );
}

export default App;
