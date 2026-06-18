export const metadata = { title: "broke — access" };

export default function NoAccessPage() {
  return (
    <main style={{ minHeight: "100vh", display: "grid", placeItems: "center", padding: "2rem", textAlign: "center" }}>
      <div style={{ maxWidth: 420 }}>
        <h1 style={{ fontSize: 28, fontWeight: 800, letterSpacing: "-0.02em" }}>broke</h1>
        <p style={{ opacity: 0.75, marginTop: 12, lineHeight: 1.6 }}>
          You're signed in, but your account doesn't have broke access yet. broke is a membership —
          manage it from your ThinkBigJoe account.
        </p>
        <a
          href="https://thinkbigjoe.com/portal/account"
          style={{ display: "inline-block", marginTop: 20, padding: "11px 18px", borderRadius: 999, background: "#16a34a", color: "white", fontWeight: 700, textDecoration: "none", fontSize: 14 }}
        >
          Go to ThinkBigJoe account
        </a>
      </div>
    </main>
  );
}
