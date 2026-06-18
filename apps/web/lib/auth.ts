import { betterAuth } from "better-auth";
import { nextCookies } from "better-auth/next-js";
import { Pool } from "pg";

/**
 * broke.finance auth — intentionally configured IDENTICALLY to thinkbigjoe's
 * (same BETTER_AUTH_SECRET + same Neon DB + same `better_auth` schema), so the
 * user table is SHARED: anyone who signed up on thinkbigjoe can log in here with
 * the same credentials. Keep this in lockstep with thinkbigjoe/src/lib/auth.ts.
 */
const baseURL =
  process.env.BETTER_AUTH_URL ||
  (process.env.VERCEL_PROJECT_PRODUCTION_URL
    ? `https://${process.env.VERCEL_PROJECT_PRODUCTION_URL}`
    : undefined) ||
  "http://localhost:3000";

// Cross-domain SSO from thinkbigjoe posts here, so trust that origin.
const trustedOrigins = [
  "https://thinkbigjoe.com",
  "https://www.thinkbigjoe.com",
  ...(process.env.THINKBIGJOE_URL ? [process.env.THINKBIGJOE_URL] : []),
];

export const auth = betterAuth({
  baseURL,
  trustedOrigins,
  secret: process.env.BETTER_AUTH_SECRET,
  database: new Pool({
    // Neon DIRECT (unpooled) endpoint so the search_path startup option sticks.
    connectionString:
      process.env.DATABASE_URL_UNPOOLED ||
      process.env.POSTGRES_URL_NON_POOLING ||
      process.env.DATABASE_URL ||
      process.env.POSTGRES_URL ||
      "",
    // Same isolated schema thinkbigjoe uses, so the user/session tables are shared.
    options: "-c search_path=better_auth",
  }),
  emailAndPassword: {
    enabled: true,
  },
  plugins: [
    // nextCookies must stay last.
    nextCookies(),
  ],
});
