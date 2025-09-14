import React, { useState, useEffect } from "react";
import axios from "axios";

function Results() {
  const [results, setResults] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem("token");
    axios
      .get("http://127.0.0.1:8000/api/results/", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => setResults(res.data))
      .catch(() => alert("Error fetching results!"));
  }, []);

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
