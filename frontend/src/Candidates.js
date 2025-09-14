import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function Candidates() {
  const [candidates, setCandidates] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/"); // if not logged in, go back to login
    }

    axios
      .get("http://127.0.0.1:8000/api/candidates/", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => setCandidates(res.data))
      .catch(() => alert("Error fetching candidates!"));
  }, [navigate]);

  const voteCandidate = async (id) => {
    const token = localStorage.getItem("token");
    try {
      await axios.post(
        "http://127.0.0.1:8000/api/vote/",
        { candidate: id },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      alert("Vote cast successfully!");
      navigate("/results");
    } catch {
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
