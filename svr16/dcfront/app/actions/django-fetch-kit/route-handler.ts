import { NextRequest, NextResponse } from "next/server"
import {
  buildCookieHeader,
  buildDjangoUrl,
  buildForwardHeaders,
  DjangoFetchInput,
  DjangoHttpMethod,
  getSetCookieHeaders,
  serializeDjangoBody,
} from "./shared"

type ProxyInput = Omit<DjangoFetchInput, "headers" | "body" | "cookieHeader" | "authToken"> & {
  request: NextRequest
  path: string
}

export async function proxyNextRequestToDjango(input: ProxyInput) {
  const method = (input.method ?? input.request.method).toUpperCase() as DjangoHttpMethod
  const authToken = input.request.cookies.get("auth_token")?.value
  const cookieHeader = buildCookieHeader(
    input.request.cookies.getAll().map((cookie) => ({
      name: cookie.name,
      value: cookie.value,
    })),
  )

  const body = method === "GET" || method === "HEAD" ? undefined : await input.request.arrayBuffer()
  const serialized = serializeDjangoBody(method, body, "raw")
  const response = await fetch(buildDjangoUrl({ ...input, method }), {
    method,
    headers: buildForwardHeaders({
      incomingHeaders: input.request.headers,
      bodyHeaders: serialized.headers,
      cookieHeader,
      authToken,
    }),
    body: serialized.body,
    credentials: "include",
    cache: input.cache ?? "no-store",
  })

  return toNextResponse(response)
}

export async function toNextResponse(upstream: Response) {
  const response = new NextResponse(upstream.body, {
    status: upstream.status,
    statusText: upstream.statusText,
  })

  upstream.headers.forEach((value, key) => {
    if (key.toLowerCase() !== "set-cookie") {
      response.headers.set(key, value)
    }
  })

  for (const rawCookie of getSetCookieHeaders(upstream)) {
    response.headers.append("set-cookie", rawCookie)
  }

  return response
}
