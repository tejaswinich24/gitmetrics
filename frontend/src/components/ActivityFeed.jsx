function formatEventType(type) {
  const map = {
    PushEvent: "pushed to",
    PullRequestEvent: "opened/updated a PR on",
    IssuesEvent: "opened/updated an issue on",
    WatchEvent: "starred",
    ForkEvent: "forked",
    CreateEvent: "created",
    DeleteEvent: "deleted a branch/tag on",
  };
  return map[type] || type;
}

export default function ActivityFeed({ events, connected }) {
  return (
    <div style={{ marginTop: "24px" }}>
      <h3>
        Live Activity{" "}
        <span style={{ fontSize: "12px", color: connected ? "limegreen" : "gray" }}>
          {connected ? "● live" : "● connecting..."}
        </span>
      </h3>
      {events.length === 0 && <p style={{ color: "gray" }}>Waiting for new activity...</p>}
      <ul style={{ listStyle: "none", padding: 0 }}>
        {events.map((e) => (
          <li
            key={e.id}
            style={{
              padding: "8px",
              borderBottom: "1px solid #333",
              fontSize: "14px",
            }}
          >
            {formatEventType(e.type)} <strong>{e.repo}</strong>
            <span style={{ color: "gray", marginLeft: "8px", fontSize: "12px" }}>
              {new Date(e.created_at).toLocaleTimeString()}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}