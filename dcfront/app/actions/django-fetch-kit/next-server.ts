"use server"

import { cookies, headers } from "next/headers"
import parseSetCookie from "@/app/lib/parseCookie"
import {
  buildCookieHeader,
  buildDjangoUrl,
  buildForwardHeaders,
  DjangoFetchInput,
  DjangoHttpMethod,
  getSetCookieHeaders,
  readJsonOrThrow,
  serializeDjangoBody,
} from "./shared"

type NextDjangoFetchInput = DjangoFetchInput & {
  browserFingerprint?: string | null
  syncCookies?: boolean
}

export async function djangoServerFetch(input: NextDjangoFetchInput) {
  const method = (input.method ?? "GET").toUpperCase() as DjangoHttpMethod
  const cookieStore = await cookies()
  const requestHeaders = await headers()
  const authToken = input.authToken ?? cookieStore.get("auth_token")?.value

  if (input.browserFingerprint) {
    const current = cookieStore.get("_polz")?.value
    if (current !== input.browserFingerprint) {
      cookieStore.set("_polz", input.browserFingerprint, fingerprintCookieOptions())
    }
  }

  const cookieHeader =
    input.cookieHeader ??
    buildCookieHeader(cookieStore.getAll(), {
      _polz: input.browserFingerprint,
    })

  const serialized = serializeDjangoBody(method, input.body, input.bodyKind)
  const forwardHeaders = buildForwardHeaders({
    incomingHeaders: requestHeaders,
    extraHeaders: input.headers,
    bodyHeaders: serialized.headers,
    cookieHeader,
    authToken,
  })

  const response = await fetch(buildDjangoUrl(input), {
    method,
    headers: forwardHeaders,
    body: serialized.body,
    credentials: "include",
    cache: input.cache ?? "no-store",
    next: input.next,
  })

  if (input.syncCookies ?? true) {
    for (const rawCookie of getSetCookieHeaders(response)) {
      cookieStore.set(parseSetCookie(rawCookie))
    }
  }

  if (response.status === 401) {
    cookieStore.delete("auth_token")
  }

  return response
}

export async function djangoJson<T>(input: NextDjangoFetchInput) {
  const response = await djangoServerFetch(input)
  return readJsonOrThrow<T>(response)
}

export async function djangoGet<T>(
  path: string,
  query?: NextDjangoFetchInput["query"],
  options: Omit<NextDjangoFetchInput, "path" | "method" | "query" | "body"> = {},
) {
  return djangoJson<T>({
    ...options,
    method: "GET",
    path,
    query,
  })
}

export async function djangoPostJson<T>(
  path: string,
  body?: unknown,
  options: Omit<NextDjangoFetchInput, "path" | "method" | "body" | "bodyKind"> = {},
) {
  return djangoJson<T>({
    ...options,
    method: "POST",
    path,
    body,
    bodyKind: "json",
  })
}

export async function djangoCommand<T>(
  command: string,
  params: unknown = {},
  options: Omit<NextDjangoFetchInput, "path" | "method" | "query" | "body"> = {},
) {
  return djangoGet<T>("/c/", { u: command, p: JSON.stringify(params) }, options)
}

function fingerprintCookieOptions() {
  return {
    path: "/",
    sameSite: "lax" as const,
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    maxAge: 60 * 60 * 24 * 365,
  }
}
