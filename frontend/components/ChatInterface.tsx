"use client";

import { useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";
const API_KEY = process.env.NEXT_PUBLIC_API_KEY ?? "dev-key";

export default function ChatInterface() {
  const [message, setMessage] = useState("");
  const [jobId, setJobId] = useState("");
  const [reply, setReply] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  async function send() {
    setReply([]);
    setLoading(true);
    const res = await fetch(`${API_BASE}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "x-api-key": API_KEY },
      body: JSON.stringify({ message, job_id: jobId ? Number(jobId) : undefined })
    });
    if (!res.body) {
      setLoading(false);
      return;
    }
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      const chunk = decoder.decode(value);
      const tokens = chunk
        .split("\n")
        .filter((line) => line.startsWith("data:"))
        .map((line) => line.replace("data:", "").trim())
        .filter(Boolean);
      if (tokens.length) setReply((prev) => [...prev, ...tokens]);
    }
    setLoading(false);
  }

  return (
    <main className="container" style={{ padding: "36px 0 64px" }}>
      <section className="panel" style={{ padding: 20 }}>
        <h2 style={{ marginTop: 0 }}>AI Explanation Chat</h2>
        <p className="muted">
          Ask follow-up questions. Add `job id` for context-aware explanation of a completed analysis.
        </p>

        <div style={{ display: "grid", gap: 10, marginBottom: 10 }}>
          <input
            className="input"
            value={jobId}
            onChange={(e) => setJobId(e.target.value)}
            placeholder="Optional job id (e.g. 5)"
          />
          <input
            className="input"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Ask why this movie looks suspicious..."
          />
        </div>
        <button className="btn btn-primary" onClick={send} disabled={loading || !message.trim()}>
          {loading ? "Streaming..." : "Send"}
        </button>
      </section>

      <section className="panel" style={{ marginTop: 14, padding: 20, minHeight: 180 }}>
        <h4 style={{ marginTop: 0 }}>Live Response</h4>
        {reply.length ? (
          <p style={{ lineHeight: 1.75 }}>{reply.join(" ")}</p>
        ) : (
          <p className="muted">No response yet. Send a message to start streaming output.</p>
        )}
      </section>
    </main>
  );
}
