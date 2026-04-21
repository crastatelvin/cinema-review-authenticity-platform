"use client";

import { useEffect, useMemo, useState } from "react";
import { getAnalysis } from "../../../lib/api";
import AnalysisDashboard from "../../../components/AnalysisDashboard";

export default function AnalyzePage({ params }: { params: { jobId: string } }) {
  const [status, setStatus] = useState("loading");
  const [result, setResult] = useState<any | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    let stopped = false;
    const tick = async () => {
      try {
        const response = await getAnalysis(params.jobId);
        if (stopped) return;
        setStatus(response.status);
        if (response.status === "completed") {
          setResult(response.result);
          return;
        }
        if (response.status === "failed") {
          setError(response.error_message ?? "Analysis failed");
          return;
        }
      } catch (err) {
        if (!stopped) setError(err instanceof Error ? err.message : "Failed to fetch status");
      }
      if (!stopped) setTimeout(tick, 2500);
    };
    tick();
    return () => {
      stopped = true;
    };
  }, [params.jobId]);

  if (result) return <AnalysisDashboard data={result} />;

  return (
    <main className="container" style={{ padding: "36px 0 64px" }}>
      <section className="panel" style={{ padding: 24 }}>
        <h2 style={{ marginTop: 0 }}>Analysis Job #{params.jobId}</h2>
        <p className="muted">Status: {status}</p>
        {error ? <p style={{ color: "var(--danger)" }}>{error}</p> : null}
        {!error && status !== "completed" ? (
          <p className="muted">Running dynamic checks. This page auto-refreshes until results are ready.</p>
        ) : null}
      </section>
    </main>
  );
}
