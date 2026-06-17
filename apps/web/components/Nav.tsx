"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { MODE } from "@/lib/mock";

const LINKS = [
  { href: "/", label: "Home" },
  { href: "/trader", label: "Trader" },
  { href: "/digest", label: "Digest" },
  { href: "/activity", label: "Activity" },
];

export function Nav() {
  const path = usePathname();
  return (
    <nav
      style={{
        display: "flex",
        alignItems: "center",
        gap: 20,
        padding: "12px 24px",
        borderBottom: "1px solid var(--border)",
        background: "var(--surface)",
        position: "sticky",
        top: 0,
        zIndex: 10,
      }}
    >
      <Link href="/" style={{ fontWeight: 500, fontSize: 18, marginRight: 8 }}>
        broke
      </Link>
      <div style={{ display: "flex", gap: 18, flex: 1 }}>
        {LINKS.filter((l) => l.href !== "/").map((l) => {
          const active = path === l.href;
          return (
            <Link
              key={l.href}
              href={l.href}
              style={{
                fontSize: 14,
                color: active ? "var(--text)" : "var(--muted)",
                borderBottom: active ? "2px solid var(--info)" : "2px solid transparent",
                paddingBottom: 2,
              }}
            >
              {l.label}
            </Link>
          );
        })}
      </div>
      <span
        style={{
          fontSize: 12,
          color: "var(--amber)",
          border: "1px solid rgba(210,153,34,0.4)",
          borderRadius: 999,
          padding: "2px 10px",
        }}
      >
        ● {MODE.toUpperCase()}
      </span>
    </nav>
  );
}
