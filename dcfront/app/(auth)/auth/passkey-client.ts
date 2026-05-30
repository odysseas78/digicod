"use client";

import { startAuthentication } from "@simplewebauthn/browser";

export async function loginWithPasskey() {
  const optionsRes = await fetch("/auth/passkeys/login/options/", {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!optionsRes.ok) {
    throw new Error("Passkey-Optionen konnten nicht geladen werden.");
  }

  const optionsJSON = await optionsRes.json();

  const authentication = await startAuthentication({ optionsJSON });

  const verifyRes = await fetch("/auth/passkeys/login/verify/", {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(authentication),
  });

  const result = await verifyRes.json().catch(() => null);

  if (!verifyRes.ok || !result?.verified) {
    throw new Error(result?.detail || "Passkey Login fehlgeschlagen.");
  }

  return result;
}