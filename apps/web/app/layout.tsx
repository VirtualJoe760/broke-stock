import "./globals.css";
import type { Metadata } from "next";
import type { ReactNode } from "react";
import { Nav } from "@/components/Nav";

export const metadata: Metadata = {
  title: "broke",
  description: "AI-assisted trading platform (paper mode)",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Nav />
        {children}
      </body>
    </html>
  );
}
