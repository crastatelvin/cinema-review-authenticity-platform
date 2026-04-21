import Link from "next/link";

export default function HomePage() {
  return (
    <main style={{ padding: 24, fontFamily: "sans-serif" }}>
      <h1>Cinema Review Authenticity Platform</h1>
      <p>Use the analyze endpoint to create jobs, then open the dashboard by job id.</p>
      <p>Example: create job from API docs and visit /analyze/&lt;jobId&gt;</p>
      <Link href="/chat">Open chat</Link>
    </main>
  );
}
