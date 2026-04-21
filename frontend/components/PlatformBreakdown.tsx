export default function PlatformBreakdown({ platforms }: { platforms: Array<{ platform: string; score: number }> }) {
  return (
    <section className="panel" style={{ padding: 18 }}>
      <h4 style={{ marginTop: 0 }}>Platform Breakdown</h4>
      <ul style={{ listStyle: "none", padding: 0, margin: 0, display: "grid", gap: 10 }}>
        {platforms.map((p) => (
          <li key={p.platform} style={{ border: "1px solid var(--border)", borderRadius: 10, padding: 10 }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
              <span>{p.platform}</span>
              <strong>{p.score.toFixed(1)}</strong>
            </div>
            <div style={{ height: 8, borderRadius: 99, background: "rgba(255,255,255,0.08)" }}>
              <div
                style={{
                  width: `${Math.max(2, Math.min(100, p.score))}%`,
                  height: "100%",
                  borderRadius: 99,
                  background: "linear-gradient(90deg, var(--accent), var(--accent-2))"
                }}
              />
            </div>
          </li>
        ))}
      </ul>
    </section>
  );
}
