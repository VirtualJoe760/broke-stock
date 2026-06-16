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
