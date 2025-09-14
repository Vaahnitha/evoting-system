import React, { useState, useEffect } from "react";
import axios from "axios";

function Results() {
  const [results, setResults] = useState([]);
  const navigate = useNavigate();
  const API_URL = process.env.REACT_APP_API_URL;

  useEffect(() => {
    const token = localStorage.getItem("token");
    axios
      .get(`${API_URL}/results/`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => setResults(res.data))
      .catch(() => alert("Error fetching results!"));
  }, [navigate, API_URL]);

  return (
    <div style={{ padding: "20px" }}>
      <h2>Election Results</h2>
      <ul>
        {results.map((r, i) => (
          <li key={i}>
            {r.name}: {r.votes} votes
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Results;
