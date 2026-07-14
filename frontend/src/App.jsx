import { useState, useEffect } from "react";
import axios from "axios";
import { useEventsPolling } from "./hooks/useEventsPolling";
import ActivityFeed from "./components/ActivityFeed";

function App() {
  const [username, setUsername] = useState("torvalds");
  const [inputValue, setInputValue] = useState("torvalds");
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const { events, connected } = useEventsPolling(username);

  useEffect(() => {
    setLoading(true);
    setError(null);
    axios
      .get(`${import.meta.env.VITE_API_URL}/api/user/${username}/summary`)
      .then((res) => {
        setSummary(res.data);
        setLoading(false);
      })
      .catch((err) => {
        setError("Could not load data for this user.");
        setLoading(false);
      });
  }, [username]);

  const handleSearch = (e) => {
    e.preventDefault();
    if (inputValue.trim()) {
      setUsername(inputValue.trim());
    }
  };

  return (
    <div style={{ maxWidth: "800px", margin: "40px auto", fontFamily: "sans-serif" }}>
      <h1>GitMetrics</h1>
      <form onSubmit={handleSearch} style={{ marginBottom: "20px" }}>
        <input
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Enter GitHub username"
          style={{ padding: "8px", width: "250px" }}
        />
        <button type="submit" style={{ padding: "8px 16px", marginLeft: "8px" }}>
          Search
        </button>
      </form>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {summary && !loading && summary.profile && (
        <div>
          <h2>{summary.profile.login}</h2>
          <p>{summary.profile.bio}</p>
          <p>
            Followers: {summary.profile.followers} | Public repos: {summary.profile.public_repos}
          </p>
          <p style={{ fontSize: "12px", color: "gray" }}>
            Cached: {summary.cached ? "yes" : "no"} | Fetched at: {summary.fetched_at}
          </p>
        </div>
      )}

      <ActivityFeed events={events} connected={connected} />
    </div>
  );
}

export default App;