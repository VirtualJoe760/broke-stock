import { headers as nextHeaders } from "next/headers";
import { redirect } from "next/navigation";

import { auth } from "./auth";
import { hasBrokeAccess } from "./broke-access";

/**
 * Gate for every broke page: must have a (shared) better-auth session AND broke membership.
 * No session → /login. Session but no membership → /no-access. Call at the top of each
 * protected page. Mirrors thinkbigjoe/src/lib/require-broke-access.ts.
 */
export async function requireBrokeAccess(): Promise<{ email: string; name: string }> {
  const session = await auth.api.getSession({ headers: await nextHeaders() });
  const email = session?.user?.email;
  if (!session) redirect("/login");
  if (!hasBrokeAccess(email)) redirect("/no-access");
  return { email: email as string, name: session.user?.name ?? "" };
}
