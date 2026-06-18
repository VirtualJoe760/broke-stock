import { promises as fs } from "fs";
import path from "path";
import { aiActivity as sampleActivity, type AiActivity, type ActivityType } from "@/lib/mock";

export const dynamic = "force-dynamic";

const TYPE_META: Record<string, { label: string; color: string }> = {
  signal: { label: "Scored", color: "var(--muted)" },
  proposed: { label: "Proposed", color: "var(--info)" },
  approved: { label: "Approved", color: "var(--green)" },
  rejected: { label: "Rejected", color: "var(--red)" },
  filled: { label: "Filled", color: "var(--green)" },
  closed: { label: "Closed", color: "var(--amber)" },
};

function outcomeColor(o: string): string {
  if (o.includes("+")) return "var(--green)";
  if (o.includes("-") || o === "Blocked" || o === "Rejected") return "var(--red)";
  return "var(--muted)";
}

// Render timestamps as 12-hour Pacific time, e.g. "Jun 17, 2:17 PM PDT".
function formatTs(ts: string): string {
  const iso = ts.includes("T") ? ts : ts.replace(" ", "T") + "Z";
  const d = new Date(iso);
  if (isNaN(d.getTime())) return ts;
  return new Intl.DateTimeFormat("en-US", {
    timeZone: "America/Los_Angeles",
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
    hour12: true,
    timeZoneName: "short",
  }).format(d);
}

async function loadActivity(): Promise<{ data: AiActivity[]; live: boolean }> {
  try {
    const raw = await fs.readFile(path.join(process.cwd(), "lib", "live-activity.json"), "utf8");
    const data = JSON.parse(raw);
    if (Array.isArray(data) && data.length > 0) return { data, live: true };
  } catch {
    // no live feed yet — fall back to the sample
  }
  return { data: sampleActivity, live: false };
}

export default async function Activity() {
  const { data, live } = await loadActivity();

  return (
    <div className="container">
      <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
        <h1 style={{ fontWeight: 500 }}>AI activity</h1>
        <span
          style={{
            fontSize: 12,
            padding: "2px 10px",
            borderRadius: 999,
            color: live ? "var(--green)" : "var(--muted)",
            border: `1px solid ${live ? "var(--green)" : "var(--border)"}`,
          }}
        >
          {live ? "● live (paper)" : "sample"}
        </span>
      </div>
      <p className="muted" style={{ marginTop: -2, maxWidth: 660 }}>
        Every action the AI takes autonomously — what it did, the reasoning it reached, and how it
        turned out. Play money; not investment advice. The trail:{" "}
        <strong>score → decide → fill → outcome</strong>. Results shown are real — wins and losses.
      </p>

      <div style={{ marginTop: 24, display: "flex", flexDirection: "column", gap: 12 }}>
        {data.map((a, i) => {
          const meta = TYPE_META[a.type as ActivityType] ?? { label: a.type, color: "var(--muted)" };
          return (
            <div key={i} className="card" style={{ display: "flex", gap: 16, alignItems: "flex-start" }}>
              <div style={{ minWidth: 132 }}>
                <div className="muted" style={{ fontSize: 12 }}>{formatTs(a.ts)}</div>
                <span
                  style={{
                    display: "inline-block",
                    marginTop: 6,
                    fontSize: 12,
                    color: meta.color,
                    border: `1px solid ${meta.color}`,
                    borderRadius: 999,
                    padding: "1px 10px",
                  }}
                >
                  {meta.label}
                </span>
              </div>
              <div style={{ flex: 1 }}>
                <div style={{ fontWeight: 500 }}>
                  {a.symbol} — {a.action}
                </div>
                <div className="muted" style={{ fontSize: 14, lineHeight: 1.6, marginTop: 4 }}>
                  {a.reasoning}
                </div>
              </div>
              {a.outcome && (
                <div style={{ color: outcomeColor(a.outcome), fontSize: 13, whiteSpace: "nowrap" }}>
                  {a.outcome}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
