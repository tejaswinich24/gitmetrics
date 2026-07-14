import { useMemo } from "react";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
} from "recharts";

function groupEventsByDay(events) {
  const counts = {};

  events.forEach((e) => {
    const date = new Date(e.created_at);
    const key = date.toLocaleDateString("en-CA"); // YYYY-MM-DD, sortable
    counts[key] = (counts[key] || 0) + 1;
  });

  return Object.entries(counts)
    .map(([date, count]) => ({ date, count }))
    .sort((a, b) => new Date(a.date) - new Date(b.date));
}

export default function ContributorTrend({ events }) {
  const data = useMemo(() => groupEventsByDay(events), [events]);

  if (!events || events.length === 0) {
    return (
      <div style={{ marginTop: "24px" }}>
        <h3>Activity Trend</h3>
        <p style={{ color: "gray" }}>No activity data yet.</p>
      </div>
    );
  }

  return (
    <div style={{ marginTop: "24px" }}>
      <h3>Activity Trend</h3>
      <ResponsiveContainer width="100%" height={220}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#333" />
          <XAxis dataKey="date" stroke="#888" fontSize={12} />
          <YAxis allowDecimals={false} stroke="#888" fontSize={12} />
          <Tooltip />
          <Line
            type="monotone"
            dataKey="count"
            stroke="#61dafb"
            strokeWidth={2}
            dot={{ r: 3 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}