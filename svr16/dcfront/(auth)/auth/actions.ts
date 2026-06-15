"use server";

import { z } from "zod";

export type AuthMode = "login" | "register";

export type AuthState = {
  ok: boolean;
  message?: string;
  errors?: {
    email?: string[];
  };
};

const EmailSchema = z.object({
  email: z.string().trim().email("Bitte gültige E-Mail eingeben."),
  mode: z.enum(["login", "register"]),
});

export async function emailAuthAction(
  prevState: AuthState,
  formData: FormData
): Promise<AuthState> {
  const parsed = EmailSchema.safeParse({
    email: formData.get("email"),
    mode: formData.get("mode"),
  });

  if (!parsed.success) {
    return {
      ok: false,
      errors: parsed.error.flatten().fieldErrors,
      message: "Bitte Eingaben prüfen.",
    };
  }

  const { email, mode } = parsed.data;

  const endpoint =
    mode === "register"
      ? `${process.env.DJANGO_API_URL}/api/auth/register/email/`
      : `${process.env.DJANGO_API_URL}/api/auth/login/magic-link/`;

  const res = await fetch(endpoint, {
    method: "POST",
    cache: "no-store",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email }),
  });

  if (!res.ok) {
    const data = await res.json().catch(() => null);

    return {
      ok: false,
      message:
        data?.detail ||
        (mode === "register"
          ? "Registrierung konnte nicht gestartet werden."
          : "Login-Link konnte nicht gesendet werden."),
    };
  }

  return {
    ok: true,
    message:
      mode === "register"
        ? "Registrierungs-Link wurde gesendet."
        : "Login-Link wurde gesendet.",
  };
}