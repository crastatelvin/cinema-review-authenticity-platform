import AuthenticityScore from "./AuthenticityScore";
import PlatformBreakdown from "./PlatformBreakdown";
import FlaggedReviewList from "./FlaggedReviewList";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid
} from "recharts";

export default function AnalysisDashboard({ data }: { data: any }) {
  return (
    <main className="container" style={{ padding: "36px 0 64px" }}>
      <h2 style={{ marginTop: 0 }}>Live Analysis Dashboard</h2>
      <p className="muted" style={{ marginTop: -8 }}>
        Final score and per-platform signal distribution from the latest completed job.
      </p>

      <div style={{ display: "grid", gap: 14, gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))" }}>
        <AuthenticityScore score={data.authenticity_score} />
        <PlatformBreakdown platforms={data.platforms} />
      </div>

      <section className="panel" style={{ marginTop: 14, padding: 18 }}>
        <h4 style={{ marginTop: 0 }}>Platform Score Chart</h4>
        <div style={{ width: "100%", height: 280 }}>
          <ResponsiveContainer>
            <BarChart data={data.platforms}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.12)" />
              <XAxis dataKey="platform" stroke="#bfc9e9" />
              <YAxis domain={[0, 100]} stroke="#bfc9e9" />
              <Tooltip
                contentStyle={{
                  background: "#0f1629",
                  border: "1px solid rgba(155,183,255,0.28)",
                  borderRadius: 10
                }}
              />
              <Bar dataKey="score" fill="url(#scoreGradient)" radius={[8, 8, 0, 0]} />
              <defs>
                <linearGradient id="scoreGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#6ca6ff" stopOpacity={1} />
                  <stop offset="95%" stopColor="#69ffd9" stopOpacity={0.7} />
                </linearGradient>
              </defs>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </section>

      <FlaggedReviewList />
    </main>
  );
}
