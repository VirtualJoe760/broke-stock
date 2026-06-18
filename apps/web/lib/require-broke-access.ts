import { headers as nextHeaders } from "next/headers";
import { redirect } from "next/navigation";

import { auth } from "./auth";
import { hasBrokeAccess } from "./broke-access";

const THINKBIGJOE_URL = process.env.THINKBIGJOE_URL || "https://thinkbigjoe.com";

/**
 * Gate for every broke page: must have a (shared) better-auth session AND broke membership.
 * broke has NO public signup — unauthenticated visitors are funneled to thinkbigjoe to create
 * an account (?from=broke shows them why). Session but no membership → /no-access. Mirrors
 * thinkbigjoe/src/lib/require-broke-access.ts.
 */
export async function requireBrokeAccess(): Promise<{ email: string; name: string }> {
  const session = await auth.api.getSession({ headers: await nextHeaders() });
  const email = session?.user?.email;
  if (!session) redirect(`${THINKBIGJOE_URL}/login?from=broke`);
  if (!hasBrokeAccess(email)) redirect("/no-access");
  return { email: email as string, name: session.user?.name ?? "" };
}
