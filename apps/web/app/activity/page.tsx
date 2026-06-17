import { aiActivity, type ActivityType } from "@/lib/mock";

const TYPE_META: Record<ActivityType, { label: string; color: string }> = {
  signal: { label: "Scored", color: "var(--muted)" },
  proposed: { label: "Proposed", color: "var(--info)" },
  approved: { label: "Approved", color: "var(--green)" },
  rejected: { label: "Rejected", color: "var(--red)" },
  filled: { label: "Filled", color: "var(--green)" },
  closed: { label: "Closed", color: "var(--amber)" },
};

function outcomeColor(o: string): string {
  if (o.includes("+")) return "var(--green)";
  if (o.startsWith("Closed -") || o.includes("-")) return "var(--red)";
  return "var(--muted)";
}

export default function Activity() {
  return (
    <div className="container">
      <h1 style={{ fontWeight: 500 }}>AI activity</h1>
      <p className="muted" style={{ marginTop: -8, maxWidth: 640 }}>
        Every action the AI takes — what it did, the reasoning it reached, and how it turned out.
        Paper mode; nothing here is investment advice. The trail: <strong>score → propose → you
        approve → fill → outcome</strong>.
      </p>

      <div style={{ marginTop: 24, display: "flex", flexDirection: "column", gap: 12 }}>
        {aiActivity.map((a, i) => {
          const meta = TYPE_META[a.type];
          return (
            <div key={i} className="card" style={{ display: "flex", gap: 16, alignItems: "flex-start" }}>
              <div style={{ minWidth: 132 }}>
                <div className="muted" style={{ fontSize: 12 }}>{a.ts}</div>
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
