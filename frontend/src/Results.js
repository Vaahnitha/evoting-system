import React, { useState, useEffect } from "react";
import { resultsAPI } from "./services/api";
import { useNavigate } from "react-router-dom";

function Results() {
  const [results, setResults] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    resultsAPI
      .getResults()
      .then((res) => setResults(res.data))
      .catch(() => alert("Error fetching results!"));
  }, [navigate]);

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
