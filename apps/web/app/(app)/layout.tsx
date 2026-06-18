import type { ReactNode } from "react";

import { Nav } from "@/components/Nav";
import { requireBrokeAccess } from "@/lib/require-broke-access";

// Gates every app page: requires a (shared) better-auth session + broke membership.
// /login and /no-access live outside this group, so they don't loop.
export default async function AppLayout({ children }: { children: ReactNode }) {
  await requireBrokeAccess();
  return (
    <>
      <Nav />
      {children}
    </>
  );
}
