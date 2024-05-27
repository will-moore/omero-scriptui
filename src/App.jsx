import React, { useState, useEffect } from 'react';
import './App.css'

function App() {

  const [projects, setProjects] = useState([]);

  // Construct the API projects URL
  const projectsUrl = BASE_OMEROWEB_URL + 'api/v0/m/projects/';

  useEffect(() => {
    const fetchData = async () => {
      let cors_headers = { mode: 'cors', credentials: 'include' };
      let rspJson = await fetch(projectsUrl, cors_headers).then(rsp => rsp.json());
      setProjects(rspJson.data)
    };

    fetchData();
  }, []);

  return (
    <>
    <div>Total: {projects.length} projects...</div>
      <ul>
          { projects.map(p => <li key={p['@id']}> {p.Name} (ID: {p['@id']})</li>)}
      </ul>
    </>
  )
}

export default App
