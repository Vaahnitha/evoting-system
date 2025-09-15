import React, { useState, useEffect } from "react";
import { candidatesAPI, voteAPI } from "./services/api";
import { useNavigate } from "react-router-dom";

// API base handled in services/api.js via env vars

function Candidates() {
  const [candidates, setCandidates] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/"); // If not logged in, go back to login
      return;
    }

    candidatesAPI
      .getCandidates()
      .then((res) => setCandidates(res.data))
      .catch((err) => {
        console.error(err);
        alert("Error fetching candidates!");
      });
  }, [navigate]);

  const voteCandidate = async (id) => {
    const token = localStorage.getItem("token");
    try {
      await voteAPI.castVote(id);
      alert("Vote cast successfully!");
      navigate("/results");
    } catch (err) {
      console.error(err);
      alert("Error casting vote (maybe already voted).");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Candidates</h2>
      <ul>
        {candidates.map((c) => (
          <li key={c.id}>
            {c.name} ({c.department})
            <button onClick={() => voteCandidate(c.id)}>Vote</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Candidates;
