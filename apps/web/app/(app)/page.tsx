import Link from "next/link";
import { MODE } from "@/lib/mock";

export default function Home() {
  return (
    <div className="container">
      <div className={`mode-banner ${MODE === "live" ? "live" : ""}`}>
        <span>● {MODE.toUpperCase()} — simulated funds</span>
        <span>broke</span>
      </div>

      <h1 style={{ fontWeight: 500 }}>broke</h1>
      <p className="muted" style={{ marginTop: -8 }}>
        AI-assisted trading — the analyst proposes, you approve, the risk gate guards. Paper-first.
      </p>

      <div className="row" style={{ marginTop: 24 }}>
        <Link href="/trader" className="card" style={{ flex: 1, minWidth: 260 }}>
          <h2 style={{ fontWeight: 500, margin: "0 0 6px" }}>Trader cockpit →</h2>
          <p className="muted" style={{ margin: 0 }}>
            Monitor &amp; act: positions, AI proposals, risk panel, kill switch.
          </p>
        </Link>
        <Link href="/digest" className="card" style={{ flex: 1, minWidth: 260 }}>
          <h2 style={{ fontWeight: 500, margin: "0 0 6px" }}>Financial digest →</h2>
          <p className="muted" style={{ margin: 0 }}>
            Understand &amp; decide: AI daily brief, scored news, position theses.
          </p>
        </Link>
      </div>
    </div>
  );
}
