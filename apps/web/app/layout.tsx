import "./globals.css";
import type { Metadata } from "next";
import type { ReactNode } from "react";

export const metadata: Metadata = {
  title: "broke",
  description: "AI-assisted trading platform (paper mode)",
};

// Bare shell. The Nav + the auth/broke-access gate live in the (app) group layout,
// so /login and /no-access render without the app chrome or the gate.
export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
