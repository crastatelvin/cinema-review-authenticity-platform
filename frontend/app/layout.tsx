import type { ReactNode } from "react";
import Link from "next/link";
import "./globals.css";

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="nav">
          <div className="container nav-inner">
            <Link href="/" className="brand">
              Cinema Authenticity AI
            </Link>
            <nav className="nav-links">
              <Link href="/">Home</Link>
              <Link href="/chat">Chat</Link>
            </nav>
          </div>
        </header>
        {children}
      </body>
    </html>
  );
}
