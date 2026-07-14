import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from "recharts";

const COLORS = [
  "#61dafb", "#f0db4f", "#3178c6", "#e34c26", "#4F5D95",
  "#89e051", "#b07219", "#00ADD8", "#701516", "#c22d40",
  "#563d7c", "#f34b7d", "#178600", "#dea584", "#41b883"
];

export default function LanguageBreakdown({ languages }) {
  if (!languages || Object.keys(languages).length === 0) {
    return (
      <div style={{ marginTop: "24px" }}>
        <h3>Language Breakdown</h3>
        <p style={{ color: "gray" }}>No language data available.</p>
      </div>
    );
  }

  const totalBytes = Object.values(languages).reduce((sum, v) => sum + v, 0);

  const data = Object.entries(languages)
    .map(([name, bytes]) => ({
      name,
      value: bytes,
      percent: ((bytes / totalBytes) * 100).toFixed(1),
    }))
    .sort((a, b) => b.value - a.value)
    .slice(0, 10); // top 10 languages only, keeps chart readable

  return (
    <div style={{ marginTop: "24px" }}>
      <h3>Language Breakdown</h3>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={data}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={100}
            label={({ name, percent }) => `${name} ${percent}%`}
          >
            {data.map((entry, index) => (
              <Cell key={entry.name} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip
            formatter={(value, name, props) => [
              `${props.payload.percent}%`,
              name,
            ]}
          />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}