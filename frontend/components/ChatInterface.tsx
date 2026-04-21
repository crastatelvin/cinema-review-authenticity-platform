"use client";

import { useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";
const API_KEY = process.env.NEXT_PUBLIC_API_KEY ?? "dev-key";

export default function ChatInterface() {
  const [message, setMessage] = useState("");
  const [reply, setReply] = useState("");

  async function send() {
    setReply("");
    const res = await fetch(`${API_BASE}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "x-api-key": API_KEY },
      body: JSON.stringify({ message })
    });
    if (!res.body) return;
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
        .join(" ");
      if (tokens) setReply((prev) => `${prev} ${tokens}`.trim());
    }
  }

  return (
    <main style={{ padding: 24 }}>
      <h2>Chat</h2>
      <input value={message} onChange={(e) => setMessage(e.target.value)} />
      <button onClick={send}>Send</button>
      <pre>{reply}</pre>
    </main>
  );
}
