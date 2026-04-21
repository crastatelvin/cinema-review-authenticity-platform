export default function AuthenticityScore({ score }: { score: number }) {
  return <h3>Authenticity Score: {score.toFixed(1)} / 100</h3>;
}
