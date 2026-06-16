"use client";

import { useEffect, useRef, useState } from "react";
import {
  MODE,
  portfolio,
  positions,
  proposal,
  equityCurve,
  riskState,
} from "@/lib/mock";

const fmt = (n: number) =>
  n.toLocaleString("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 });

function EquityChart() {
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (!ref.current) return;
    let chart: { remove: () => void } | null = null;
    let disposed = false;
    import("lightweight-charts").then(({ createChart }) => {
      if (disposed || !ref.current) return;
      const c = createChart(ref.current, {
        height: 140,
        layout: { background: { color: "transparent" }, textColor: "#8b93a3" },
        grid: { vertLines: { visible: false }, horzLines: { color: "#232a36" } },
        rightPriceScale: { borderColor: "#232a36" },
        timeScale: { borderColor: "#232a36" },
      });
      const series = c.addLineSeries({ color: "#3fb950", lineWidth: 2 });
      const base = new Date("2025-05-01");
      series.setData(
        equityCurve.map((value, i) => {
          const d = new Date(base);
          d.setDate(base.getDate() + i);
          return { time: d.toISOString().slice(0, 10), value };
        })
      );
      c.timeScale().fitContent();
      chart = c;
    });
    return () => {
      disposed = true;
      chart?.remove();
    };
  }, []);
  return <div ref={ref} style={{ width: "100%" }} />;
}

export default function Trader() {
  const [decision, setDecision] = useState<"pending" | "approved" | "rejected">("pending");
  const [killArmed, setKillArmed] = useState(false);

  return (
    <div className="container">
      <div className={`mode-banner ${MODE === "live" ? "live" : ""}`}>
        <span>● {MODE.toUpperCase()} — simulated funds</span>
        <span>feed 12ms · engine live · NYSE open</span>
      </div>

      <div className="row" style={{ marginBottom: 16 }}>
        {[
          ["Equity", fmt(portfolio.equity), ""],
          ["Day P&L", fmt(portfolio.dayPnl), portfolio.dayPnl >= 0 ? "pos" : "neg"],
          ["Total P&L", fmt(portfolio.totalPnl), portfolio.totalPnl >= 0 ? "pos" : "neg"],
          ["Buying power", fmt(portfolio.buyingPower), ""],
        ].map(([label, value, cls]) => (
          <div className="card" key={label} style={{ flex: 1, minWidth: 150 }}>
            <div className="muted" style={{ fontSize: 13 }}>{label}</div>
            <div className={cls as string} style={{ fontSize: 22, marginTop: 4 }}>{value}</div>
          </div>
        ))}
      </div>

      <div className="card" style={{ marginBottom: 16 }}>
        <div className="muted" style={{ fontSize: 13, marginBottom: 8 }}>Equity curve · 30d</div>
        <EquityChart />
      </div>

      <div className="card" style={{ marginBottom: 16 }}>
        <div className="muted" style={{ fontSize: 13, marginBottom: 8 }}>Positions</div>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr className="muted" style={{ textAlign: "right", fontSize: 12 }}>
              <th style={{ textAlign: "left" }}>Symbol</th><th>Qty</th><th>Last</th><th>P&L</th><th>AI conf.</th>
            </tr>
          </thead>
          <tbody>
            {positions.map((p) => (
              <tr key={p.symbol} style={{ textAlign: "right", borderTop: "1px solid var(--border)" }}>
                <td style={{ textAlign: "left", padding: "8px 0" }}>{p.symbol}</td>
                <td>{p.qty}</td>
                <td>${p.last.toFixed(2)}</td>
                <td className={p.pnl >= 0 ? "pos" : "neg"}>{p.pnl >= 0 ? "+" : ""}{fmt(p.pnl)}</td>
                <td className={p.aiConfidence >= 0.6 ? "pos" : "muted"}>{Math.round(p.aiConfidence * 100)}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="card" style={{ marginBottom: 16, borderColor: "var(--info)" }}>
        <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
          <strong style={{ fontWeight: 500 }}>AI trade proposal</strong>
          <span className="muted" style={{ fontSize: 12 }}>surprise {proposal.surprise}</span>
        </div>
        <p style={{ margin: "0 0 12px" }}>
          {proposal.side === "buy" ? "Buy" : "Sell"} <strong>{proposal.qty} {proposal.symbol}</strong> — {proposal.rationale}.
        </p>
        {decision === "pending" ? (
          <div className="row">
            <button className="buy" onClick={() => setDecision("approved")}>Approve</button>
            <button className="sell" onClick={() => setDecision("rejected")}>Reject</button>
          </div>
        ) : (
          <div className={decision === "approved" ? "pos" : "neg"}>
            {decision === "approved" ? "Approved (paper) — routed to risk gate." : "Rejected."}
          </div>
        )}
      </div>

      <div className="row">
        <div className="card" style={{ flex: 1, minWidth: 240 }}>
          <div className="muted" style={{ fontSize: 13, marginBottom: 8 }}>Order ticket</div>
          <div className="row" style={{ gap: 8 }}>
            <input defaultValue="MU" style={{ flex: 1, background: "var(--bg)", color: "var(--text)", border: "1px solid var(--border)", borderRadius: 8, padding: 8 }} />
            <input defaultValue="40" style={{ width: 70, background: "var(--bg)", color: "var(--text)", border: "1px solid var(--border)", borderRadius: 8, padding: 8 }} />
          </div>
          <div className="row" style={{ gap: 8, marginTop: 8 }}>
            <button className="buy" style={{ flex: 1 }}>Buy</button>
            <button className="sell" style={{ flex: 1 }}>Sell</button>
          </div>
        </div>

        <div className="card" style={{ flex: 1, minWidth: 240 }}>
          <div className="muted" style={{ fontSize: 13, marginBottom: 8 }}>Risk</div>
          <Bar label="Gross exposure" pct={riskState.grossExposurePct} color="var(--info)" />
          <Bar label="Daily loss limit" pct={riskState.dailyLossUsedPct} color="var(--amber)" />
          <button className="kill" style={{ width: "100%", marginTop: 12 }} onClick={() => setKillArmed(true)}>
            {killArmed ? "Kill switch armed — flatten all?" : "Flatten all · kill switch"}
          </button>
        </div>
      </div>
    </div>
  );
}

function Bar({ label, pct, color }: { label: string; pct: number; color: string }) {
  return (
    <div style={{ marginBottom: 10 }}>
      <div style={{ display: "flex", justifyContent: "space-between", fontSize: 13 }}>
        <span className="muted">{label}</span><span>{pct}%</span>
      </div>
      <div style={{ height: 7, borderRadius: 99, background: "var(--bg)", marginTop: 4 }}>
        <div style={{ width: `${pct}%`, height: 7, borderRadius: 99, background: color }} />
      </div>
    </div>
  );
}
