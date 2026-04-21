import AnalysisDashboard from "../../../components/AnalysisDashboard";
import { getAnalysis } from "../../../lib/api";

export default async function AnalyzePage({
  params
}: {
  params: { jobId: string };
}) {
  const response = await getAnalysis(params.jobId);
  if (response.status !== "completed") {
    return (
      <main style={{ padding: 24, fontFamily: "sans-serif" }}>
        <h2>Analysis Job: {params.jobId}</h2>
        <p>Status: {response.status}</p>
        <p>Refresh this page while processing continues.</p>
      </main>
    );
  }
  return <AnalysisDashboard data={response.result} />;
}
