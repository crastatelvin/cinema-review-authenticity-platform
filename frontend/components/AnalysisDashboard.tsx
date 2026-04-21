import AuthenticityScore from "./AuthenticityScore";
import PlatformBreakdown from "./PlatformBreakdown";
import FlaggedReviewList from "./FlaggedReviewList";

export default function AnalysisDashboard({ data }: { data: any }) {
  return (
    <main style={{ padding: 24, fontFamily: "sans-serif" }}>
      <h2>Analysis Dashboard</h2>
      <AuthenticityScore score={data.authenticity_score} />
      <PlatformBreakdown platforms={data.platforms} />
      <FlaggedReviewList />
    </main>
  );
}
