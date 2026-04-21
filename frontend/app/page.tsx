"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { createAnalysis } from "../lib/api";

export default function HomePage() {
  const router = useRouter();
  const [query, setQuery] = useState("https://en.wikipedia.org/wiki/Oppenheimer_(film)");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function startAnalysis() {
    try {
      setLoading(true);
      setError("");
      const result = await createAnalysis(query);
      router.push(`/analyze/${result.job_id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to submit analysis");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="container" style={{ padding: "42px 0 64px" }}>
      <section className="panel" style={{ padding: 24 }}>
        <h1 style={{ marginTop: 0, fontSize: 36 }}>AI Movie Review Authenticity Analyzer</h1>
        <p className="muted" style={{ maxWidth: 760 }}>
          Enter a movie review URL (or title in your configured sources) to run a cross-signal analysis
          powered by NLP, duplicate-pattern detection, and authenticity scoring.
        </p>

        <div style={{ display: "grid", gap: 10, marginTop: 18 }}>
          <label htmlFor="query" className="muted">
            Movie URL or Query
          </label>
          <input
            id="query"
            className="input"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Paste review page URL..."
          />
        </div>

        <div style={{ display: "flex", gap: 10, marginTop: 14 }}>
          <button className="btn btn-primary" onClick={startAnalysis} disabled={loading}>
            {loading ? "Submitting..." : "Start Live Analysis"}
          </button>
          <button className="btn btn-secondary" onClick={() => router.push("/chat")}>
            Open AI Chat
          </button>
        </div>
        {error ? <p style={{ color: "var(--danger)", marginTop: 12 }}>{error}</p> : null}
      </section>

      <section style={{ display: "grid", gap: 12, marginTop: 20 }}>
        <div className="panel" style={{ padding: 16 }}>
          <strong>Live stack</strong>
          <p className="muted" style={{ marginBottom: 0 }}>
            FastAPI + Celery + PostgreSQL/pgvector + Next.js with streaming chat and dynamic job polling.
          </p>
        </div>
        <div className="panel" style={{ padding: 16 }}>
          <strong>Scoring approach</strong>
          <p className="muted" style={{ marginBottom: 0 }}>
            Combines transformer probability, language-aware adjustments, and platform-level signal aggregation.
          </p>
        </div>
      </section>
    </main>
  );
}
