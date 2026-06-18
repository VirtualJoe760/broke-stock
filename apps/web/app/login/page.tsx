"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

import { signIn } from "@/lib/auth-client";

const THINKBIGJOE_URL = process.env.NEXT_PUBLIC_THINKBIGJOE_URL || "https://thinkbigjoe.com";

// Sign-in only. There's no signup here — broke accounts are created on thinkbigjoe
// (shared user table), so we link there for new accounts.
export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setBusy(true);
    setError(null);
    const res = await signIn.email({ email, password });
    setBusy(false);
    if (res.error) {
      setError(res.error.message || "Couldn't sign in. Check your details and try again.");
      return;
    }
    router.push("/");
    router.refresh();
  }

  return (
    <main style={{ minHeight: "100vh", display: "grid", placeItems: "center", padding: "2rem" }}>
      <form
        onSubmit={submit}
        style={{ width: "100%", maxWidth: 360, display: "flex", flexDirection: "column", gap: 12 }}
      >
        <h1 style={{ fontSize: 28, fontWeight: 800, letterSpacing: "-0.02em", marginBottom: 4 }}>broke</h1>
        <p style={{ opacity: 0.7, marginBottom: 12, fontSize: 14 }}>
          Sign in with your ThinkBigJoe account.
        </p>

        <input
          type="email"
          placeholder="Email"
          value={email}
          required
          onChange={(e) => setEmail(e.target.value)}
          style={inputStyle}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          required
          onChange={(e) => setPassword(e.target.value)}
          style={inputStyle}
        />

        {error && <p style={{ color: "#f87171", fontSize: 13 }}>{error}</p>}

        <button type="submit" disabled={busy} style={buttonStyle}>
          {busy ? "…" : "Sign in"}
        </button>

        <p style={{ opacity: 0.7, fontSize: 13, marginTop: 4 }}>
          Don&apos;t have an account?{" "}
          <a href={`${THINKBIGJOE_URL}/login?from=broke`} style={{ color: "#16a34a", fontWeight: 600 }}>
            Create one at ThinkBigJoe →
          </a>
        </p>
      </form>
    </main>
  );
}

const inputStyle: React.CSSProperties = {
  padding: "10px 12px",
  borderRadius: 10,
  border: "1px solid rgba(127,127,127,0.35)",
  background: "transparent",
  color: "inherit",
  fontSize: 14,
};
const buttonStyle: React.CSSProperties = {
  padding: "11px 12px",
  borderRadius: 10,
  border: "none",
  background: "#16a34a",
  color: "white",
  fontWeight: 700,
  fontSize: 14,
  cursor: "pointer",
};
