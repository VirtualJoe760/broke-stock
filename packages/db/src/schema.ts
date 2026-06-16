// Drizzle schema for app state (Postgres / Neon).
// Time-series ticks live in QuestDB/DuckDB, NOT here.
// See docs/01-architecture/persistence-and-events.md.

import {
  pgTable,
  pgEnum,
  uuid,
  text,
  timestamp,
  numeric,
  jsonb,
  boolean,
} from "drizzle-orm/pg-core";

export const tradingMode = pgEnum("trading_mode", ["paper", "live"]);
export const orderSide = pgEnum("order_side", ["buy", "sell"]);
export const orderType = pgEnum("order_type", ["market", "limit", "stop", "bracket"]);
export const orderStatus = pgEnum("order_status", [
  "proposed",
  "pending",
  "filled",
  "partial",
  "cancelled",
  "rejected",
]);
export const validationLevel = pgEnum("validation_level", ["L0", "L1", "L2", "L3", "L4", "L5"]);

export const accounts = pgTable("accounts", {
  id: uuid("id").defaultRandom().primaryKey(),
  mode: tradingMode("mode").notNull().default("paper"),
  broker: text("broker").notNull().default("alpaca"),
  equity: numeric("equity", { precision: 18, scale: 2 }).notNull().default("0"),
  buyingPower: numeric("buying_power", { precision: 18, scale: 2 }).notNull().default("0"),
  createdAt: timestamp("created_at", { withTimezone: true }).defaultNow().notNull(),
});

// Validation level gates capital — nothing live below L4 (see validation-methodology.md).
export const strategies = pgTable("strategies", {
  id: uuid("id").defaultRandom().primaryKey(),
  name: text("name").notNull(),
  validationLevel: validationLevel("validation_level").notNull().default("L0"),
  params: jsonb("params").notNull().default({}),
  frozen: boolean("frozen").notNull().default(false), // live uses frozen, validation-cleared params
  createdAt: timestamp("created_at", { withTimezone: true }).defaultNow().notNull(),
});

export const orders = pgTable("orders", {
  id: uuid("id").defaultRandom().primaryKey(),
  accountId: uuid("account_id")
    .notNull()
    .references(() => accounts.id),
  strategyId: uuid("strategy_id").references(() => strategies.id),
  symbol: text("symbol").notNull(),
  side: orderSide("side").notNull(),
  type: orderType("type").notNull().default("market"),
  qty: numeric("qty", { precision: 18, scale: 6 }).notNull(),
  status: orderStatus("status").notNull().default("proposed"),
  clientOrderId: text("client_order_id").notNull().unique(), // idempotent submission
  correlationId: uuid("correlation_id"), // threads signal -> intent -> order -> fill
  createdAt: timestamp("created_at", { withTimezone: true }).defaultNow().notNull(),
});

export const positions = pgTable("positions", {
  id: uuid("id").defaultRandom().primaryKey(),
  accountId: uuid("account_id")
    .notNull()
    .references(() => accounts.id),
  symbol: text("symbol").notNull(),
  qty: numeric("qty", { precision: 18, scale: 6 }).notNull().default("0"),
  avgPrice: numeric("avg_price", { precision: 18, scale: 6 }).notNull().default("0"),
  unrealizedPnl: numeric("unrealized_pnl", { precision: 18, scale: 2 }).notNull().default("0"),
  updatedAt: timestamp("updated_at", { withTimezone: true }).defaultNow().notNull(),
});

export const fills = pgTable("fills", {
  id: uuid("id").defaultRandom().primaryKey(),
  orderId: uuid("order_id")
    .notNull()
    .references(() => orders.id),
  ts: timestamp("ts", { withTimezone: true }).notNull(),
  qty: numeric("qty", { precision: 18, scale: 6 }).notNull(),
  price: numeric("price", { precision: 18, scale: 6 }).notNull(),
  fees: numeric("fees", { precision: 18, scale: 4 }).notNull().default("0"),
  slippage: numeric("slippage", { precision: 18, scale: 6 }).notNull().default("0"),
});

// Every AI decision, order, alert is logged and reconstructable (audit + compliance).
export const audit = pgTable("audit", {
  id: uuid("id").defaultRandom().primaryKey(),
  ts: timestamp("ts", { withTimezone: true }).defaultNow().notNull(),
  actor: text("actor").notNull(), // 'agent' | 'human' | 'system'
  action: text("action").notNull(),
  before: jsonb("before"),
  after: jsonb("after"),
  correlationId: uuid("correlation_id"),
});
