export default function PlatformBreakdown({ platforms }: { platforms: Array<{ platform: string; score: number }> }) {
  return (
    <section>
      <h4>Platform Breakdown</h4>
      <ul>
        {platforms.map((p) => (
          <li key={p.platform}>
            {p.platform}: {p.score}
          </li>
        ))}
      </ul>
    </section>
  );
}
