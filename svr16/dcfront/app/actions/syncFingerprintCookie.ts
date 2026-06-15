"use server"

import { cookies } from "next/headers"

function fingerprintCookieOptions() {
  return {
    path: "/",
    sameSite: "lax" as const,
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    maxAge: 60 * 60 * 24 * 365,
  }
}

export default async function syncFingerprintCookie(fingerprint?: string | null) {
  if (!fingerprint) {
    return { ok: false, changed: false }
  }

  const cookieStore = await cookies()
  const currentFingerprint = cookieStore.get("_polz")?.value

  if (currentFingerprint !== fingerprint) {
    cookieStore.set("_polz", fingerprint, fingerprintCookieOptions())
    return { ok: true, changed: true }
  }

  return { ok: true, changed: false }
}
