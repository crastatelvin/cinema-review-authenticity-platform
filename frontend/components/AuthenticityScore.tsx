export default function AuthenticityScore({ score }: { score: number }) {
  const tone = score >= 75 ? "var(--accent-2)" : score >= 50 ? "var(--accent)" : "var(--danger)";
  return (
    <section className="panel" style={{ padding: 18 }}>
      <h3 style={{ marginTop: 0 }}>Authenticity Score</h3>
      <div style={{ fontSize: 44, fontWeight: 700, color: tone }}>{score.toFixed(1)}</div>
      <p className="muted" style={{ marginBottom: 0 }}>
        Higher means review patterns look more genuine.
      </p>
    </section>
  );
}
