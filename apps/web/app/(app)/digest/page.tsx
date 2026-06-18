import { MODE, dailyBrief, news } from "@/lib/mock";

const theses = [
  {
    symbol: "NVDA",
    surprise: 0.81,
    pnl: "+12.4%",
    text: "Held since the guidance-raise event. Sentiment positive, magnitude major, and the move appears under-reacted vs. consensus.",
  },
  {
    symbol: "AVGO",
    surprise: 0.64,
    pnl: "+4.1%",
    text: "Networking-bottleneck thesis. Added on the export-data read-through; horizon weeks, confidence moderate.",
  },
];

const briefPoints = [
  { tone: "pos", text: "NVDA thesis strengthening — supply-chain read-through positive, not yet priced in." },
  { tone: "warn", text: "Watching CPI at 10:00 ET — a hot print would pressure rate-sensitive positions." },
  { tone: "neg", text: "Regional banks weak after a downgrade — no exposure, monitoring only." },
];

const media = [
  { kind: "video · 8 min", title: "The AI capex cycle, explained", tldr: "Why hyperscaler spending supports the chip thesis through 2027." },
  { kind: "article · 4 min", title: "Reading the CPI print", tldr: "Which components to watch and how each scenario hits your book." },
];

export default function Digest() {
  return (
    <div className="container">
      <div className={`mode-banner ${MODE === "live" ? "live" : ""}`}>
        <span>● {MODE.toUpperCase()} — financial digest</span>
        <span>Mon 16 Jun 2026 · markets open</span>
      </div>

      <div className="card" style={{ marginBottom: 16 }}>
        <strong style={{ fontWeight: 500 }}>AI daily brief</strong>
        <p style={{ lineHeight: 1.7 }}>{dailyBrief}</p>
        <div className="grid" style={{ gap: 8 }}>
          {briefPoints.map((b, i) => (
            <div key={i} className={b.tone === "pos" ? "pos" : b.tone === "neg" ? "neg" : ""} style={{ color: b.tone === "warn" ? "var(--amber)" : undefined, fontSize: 14 }}>
              • {b.text}
            </div>
          ))}
        </div>
      </div>

      <div className="muted" style={{ fontSize: 13, margin: "0 0 8px" }}>Why we hold what we hold</div>
      <div className="row" style={{ marginBottom: 16 }}>
        {theses.map((t) => (
          <div key={t.symbol} className="card" style={{ flex: 1, minWidth: 240 }}>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <strong style={{ fontWeight: 500 }}>{t.symbol}</strong>
              <span className="pos" style={{ fontSize: 12 }}>surprise {t.surprise}</span>
            </div>
            <p className="muted" style={{ fontSize: 14, lineHeight: 1.6 }}>{t.text}</p>
            <div style={{ display: "flex", justifyContent: "space-between", fontSize: 13 }}>
              <span className="muted">Position P&L</span><span className="pos">{t.pnl}</span>
            </div>
          </div>
        ))}
      </div>

      <div className="muted" style={{ fontSize: 13, margin: "0 0 8px" }}>Scored news feed</div>
      <div className="card" style={{ marginBottom: 16, padding: 0 }}>
        {news.map((n, i) => (
          <div key={i} style={{ display: "flex", gap: 12, padding: "14px 20px", borderTop: i ? "1px solid var(--border)" : "none" }}>
            <span style={{ fontSize: 12, padding: "2px 8px", borderRadius: 8, background: "rgba(56,139,253,0.15)", color: "var(--info)", height: "fit-content" }}>{n.ticker}</span>
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: 14 }}>{n.headline}</div>
              <div className="muted" style={{ fontSize: 12 }}>{n.source} · {n.ageMin} min ago</div>
            </div>
            <div style={{ textAlign: "right", whiteSpace: "nowrap" }}>
              <span className={n.score > 0 ? "pos" : n.score < 0 ? "neg" : ""} style={{ color: n.score === 0 ? "var(--amber)" : undefined }}>
                {n.score > 0 ? "+" : ""}{n.score.toFixed(1)}
              </span>
              <div className="muted" style={{ fontSize: 11 }}>{n.pricedIn ? "mostly priced" : "not priced in"}</div>
            </div>
          </div>
        ))}
      </div>

      <div className="muted" style={{ fontSize: 13, margin: "0 0 8px" }}>Curated for you</div>
      <div className="row">
        {media.map((m, i) => (
          <div key={i} className="card" style={{ flex: 1, minWidth: 240 }}>
            <span className="muted" style={{ fontSize: 12 }}>{m.kind}</span>
            <div style={{ fontWeight: 500, margin: "6px 0" }}>{m.title}</div>
            <div className="muted" style={{ fontSize: 13, lineHeight: 1.6 }}>AI TL;DR: {m.tldr}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
