import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const API_URL = process.env.REACT_APP_API_URL; // Make sure this is set in your .env

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    if (!username || !password) {
      alert("Please enter username and password");
      return;
    }

    try {
      const res = await axios.post(
        `${API_URL}/token/`,
        { username, password },
        { headers: { "Content-Type": "application/json" } }
      );

      // Save access token to localStorage
      localStorage.setItem("token", res.data.access);
      localStorage.setItem("refresh", res.data.refresh);

      // Redirect to candidates page
      navigate("/candidates");
    } catch (err) {
      if (err.response && err.response.data.detail) {
        alert(`Login failed: ${err.response.data.detail}`);
      } else {
        alert("Login failed! Check your username/password.");
      }
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <br />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <br />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default Login;

