const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";
const API_KEY = process.env.NEXT_PUBLIC_API_KEY ?? "dev-key";

export async function createAnalysis(query: string) {
  const res = await fetch(`${API_BASE}/api/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "x-api-key": API_KEY },
    body: JSON.stringify({ query })
  });
  if (!res.ok) throw new Error(`Analyze failed: ${res.status}`);
  return res.json();
}

export async function getAnalysis(jobId: string | number) {
  const res = await fetch(`${API_BASE}/api/analyze/${jobId}`, {
    headers: { "x-api-key": API_KEY },
    cache: "no-store"
  });
  if (!res.ok) throw new Error(`Fetch analysis failed: ${res.status}`);
  return res.json();
}
