// Mock data for the dashboards (paper mode). Replaced by the engine API later.
// See docs/02-frontend/.

export type Mode = "paper" | "live";

export interface Position {
  symbol: string;
  qty: number;
  last: number;
  pnl: number;
  aiConfidence: number; // 0..1
}

export interface Proposal {
  symbol: string;
  side: "buy" | "sell";
  qty: number;
  rationale: string;
  surprise: number;
}

export interface NewsItem {
  ticker: string;
  headline: string;
  source: string;
  ageMin: number;
  score: number; // -1..1
  pricedIn: boolean;
}

export const MODE: Mode = "paper";

export const portfolio = {
  equity: 104820,
  dayPnl: 1240,
  totalPnl: 4820,
  buyingPower: 38500,
};

export const positions: Position[] = [
  { symbol: "NVDA", qty: 120, last: 184.2, pnl: 2460, aiConfidence: 0.81 },
  { symbol: "AVGO", qty: 60, last: 242.1, pnl: 580, aiConfidence: 0.64 },
  { symbol: "AAPL", qty: 90, last: 214.55, pnl: -310, aiConfidence: 0.48 },
];

export const proposal: Proposal = {
  symbol: "MU",
  side: "buy",
  qty: 40,
  rationale: "positive earnings-call sentiment; sector momentum; sized to 3% within limits",
  surprise: 0.74,
};

export const news: NewsItem[] = [
  { ticker: "NVDA", headline: "Taiwan chip exports beat estimates", source: "Reuters", ageMin: 6, score: 0.7, pricedIn: false },
  { ticker: "SPY", headline: "Inflation print due 10:00 ET could swing rate-cut odds", source: "Bloomberg", ageMin: 22, score: 0.0, pricedIn: false },
  { ticker: "KRE", headline: "Analyst downgrades regional banks on margin pressure", source: "CNBC", ageMin: 41, score: -0.6, pricedIn: true },
];

export const dailyBrief =
  "Overnight, semiconductor names rallied on stronger Taiwan export data, lifting your two largest holdings. Futures point modestly higher, but a 10:00 ET inflation print is the day's main risk — exposure trimmed ahead of it.";

// Equity curve points (mock), 30 sessions.
export const equityCurve: number[] = [
  100000, 100400, 99800, 100600, 100500, 101200, 101000, 101900, 101600, 102400,
  102100, 103000, 102700, 103600, 103900, 104820,
];

export const riskState = {
  grossExposurePct: 63,
  dailyLossUsedPct: 18,
};

// AI decision history — every action the AI takes, the reasoning, and the outcome.
export type ActivityType = "signal" | "proposed" | "approved" | "rejected" | "filled" | "closed";

export interface AiActivity {
  ts: string;
  type: ActivityType;
  symbol: string;
  action: string; // what the AI did
  reasoning: string; // why — the conclusion it reached
  outcome?: string; // result, if resolved
}

export const aiActivity: AiActivity[] = [
  {
    ts: "2026-06-16 09:32",
    type: "filled",
    symbol: "MU",
    action: "Bought 40 MU @ $98.10 (paper)",
    reasoning: "Executed the approved proposal. Sized to 3% of equity, within position + exposure limits; bracket stop set at -7%.",
    outcome: "Open · +0.0%",
  },
  {
    ts: "2026-06-16 09:30",
    type: "proposed",
    symbol: "MU",
    action: "Proposed BUY 40 MU",
    reasoning: "Earnings-call sentiment surprise 0.74 (not yet priced in), memory-pricing tailwind, sector momentum confirmed. Confidence 0.66. Cleared the risk gate.",
    outcome: "Approved by you",
  },
  {
    ts: "2026-06-16 08:31",
    type: "signal",
    symbol: "NVDA",
    action: "Scored news: Taiwan exports beat estimates",
    reasoning: "Positive read-through but indirect and largely priced in (surprise 0.25, confidence 0.55). Below the 0.5 conviction bar.",
    outcome: "No trade",
  },
  {
    ts: "2026-06-15 15:58",
    type: "rejected",
    symbol: "KRE",
    action: "Proposed SHORT KRE — you rejected",
    reasoning: "Analyst downgrade, sentiment -0.6, but the move looked mostly priced in. You declined; logged so the agent learns the preference.",
    outcome: "Rejected",
  },
  {
    ts: "2026-06-12 10:05",
    type: "closed",
    symbol: "AVGO",
    action: "Closed AVGO at target",
    reasoning: "Networking-bottleneck thesis played out; price hit the +8% target and the trailing stop locked it in.",
    outcome: "Closed +8.1%",
  },
  {
    ts: "2026-06-11 09:34",
    type: "filled",
    symbol: "NVDA",
    action: "Bought 120 NVDA @ $171.40 (paper)",
    reasoning: "Guidance-raise event, surprise 0.81 (major, under-reacted vs consensus). High conviction; sized at the 5% cap.",
    outcome: "Open · +12.4%",
  },
];
