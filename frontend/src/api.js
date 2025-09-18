const API_URL = process.env.REACT_APP_API_URL;

export const fetchCandidates = async () => {
  try {
    const response = await fetch(`${API_URL}/candidates/`);
    if (!response.ok) throw new Error("Network response was not ok");
    return await response.json();
  } catch (err) {
    console.error("API fetch error:", err);
    return [];
  }
};
