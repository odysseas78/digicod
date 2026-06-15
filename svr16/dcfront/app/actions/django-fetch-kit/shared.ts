export type DjangoHttpMethod =
  | "GET"
  | "POST"
  | "PUT"
  | "PATCH"
  | "DELETE"
  | "HEAD"

export type QueryValue =
  | string
  | number
  | boolean
  | null
  | undefined
  | Array<string | number | boolean | null | undefined>

export type DjangoQuery = URLSearchParams | Record<string, QueryValue>

export type DjangoBodyKind = "auto" | "json" | "form" | "urlencoded" | "raw"

export type DjangoFetchInput = {
  path: string
  method?: DjangoHttpMethod
  query?: DjangoQuery
  body?: unknown
  bodyKind?: DjangoBodyKind
  baseUrl?: string
  headers?: HeadersInit
  cookieHeader?: string
  authToken?: string
  cache?: RequestCache
  next?: NextFetchRequestConfig
}

export class DjangoFetchError extends Error {
  status: number
  statusText: string
  body: string

  constructor(response: Response, body: string) {
    super(`Django request failed: HTTP ${response.status} ${body.slice(0, 500)}`)
    this.name = "DjangoFetchError"
    this.status = response.status
    this.statusText = response.statusText
    this.body = body
  }
}

export function getDjangoBaseUrl(explicitBaseUrl?: string) {
  const baseUrl =
    explicitBaseUrl ??
    process.env.DJANGO_INTERNAL_URL ??
    process.env.DJANGO_API_URL ??
    "https://front.digicod.eu"

  return baseUrl.endsWith("/") ? baseUrl : `${baseUrl}/`
}

export function buildDjangoUrl(input: DjangoFetchInput) {
  const url = new URL(stripLeadingSlash(input.path), getDjangoBaseUrl(input.baseUrl))

  if (input.query) {
    const query = toSearchParams(input.query)
    query.forEach((value, key) => {
      url.searchParams.append(key, value)
    })
  }

  return url
}

export function buildCookieHeader(
  cookies: Array<{ name: string; value: string }>,
  overrides: Record<string, string | null | undefined> = {},
) {
  const cookieMap = new Map<string, string>()

  for (const cookie of cookies) {
    cookieMap.set(cookie.name, cookie.value)
  }

  for (const [name, value] of Object.entries(overrides)) {
    if (value === null || value === undefined) continue
    cookieMap.set(name, value)
  }

  return Array.from(cookieMap.entries())
    .map(([name, value]) => `${encodeCookiePart(name)}=${encodeCookiePart(value)}`)
    .join("; ")
}

export function buildForwardHeaders(input: {
  incomingHeaders?: HeadersInit
  extraHeaders?: HeadersInit
  cookieHeader?: string
  authToken?: string
  bodyHeaders?: HeadersInit
}) {
  const headers = new Headers()

  copyAllowedHeaders(headers, input.incomingHeaders, { forwardAccept: false })
  copyAllowedHeaders(headers, input.extraHeaders, { forwardAccept: true })
  copyAllowedHeaders(headers, input.bodyHeaders)

  if (!headers.has("accept")) {
    headers.set("accept", "application/json")
  }

  if (input.cookieHeader) {
    headers.set("cookie", input.cookieHeader)
  }

  if (input.authToken && !headers.has("authorization")) {
    headers.set("authorization", `Token ${input.authToken}`)
  }

  return headers
}

export function serializeDjangoBody(
  method: DjangoHttpMethod,
  body: unknown,
  bodyKind: DjangoBodyKind = "auto",
) {
  if (method === "GET" || method === "HEAD" || body === undefined || body === null) {
    return { body: undefined, headers: undefined }
  }

  if (body instanceof FormData) {
    return { body, headers: undefined }
  }

  if (body instanceof URLSearchParams) {
    return {
      body: body.toString(),
      headers: { "content-type": "application/x-www-form-urlencoded;charset=UTF-8" },
    }
  }

  if (bodyKind === "urlencoded") {
    return {
      body: toSearchParams(body as DjangoQuery).toString(),
      headers: { "content-type": "application/x-www-form-urlencoded;charset=UTF-8" },
    }
  }

  if (bodyKind === "form") {
    const form = new FormData()
    const values = body && typeof body === "object" ? body : {}

    for (const [key, value] of Object.entries(values as Record<string, unknown>)) {
      if (value === null || value === undefined) continue
      if (value instanceof Blob) form.append(key, value)
      else form.append(key, String(value))
    }

    return { body: form, headers: undefined }
  }

  if (
    bodyKind === "raw" ||
    typeof body === "string" ||
    body instanceof Blob ||
    body instanceof ArrayBuffer ||
    body instanceof Uint8Array
  ) {
    return { body: body as BodyInit, headers: undefined }
  }

  return {
    body: JSON.stringify(body),
    headers: { "content-type": "application/json" },
  }
}

export async function readJsonOrThrow<T>(response: Response) {
  const contentType = response.headers.get("content-type") ?? ""

  if (!response.ok) {
    throw new DjangoFetchError(response, await response.text())
  }

  if (!contentType.includes("application/json")) {
    throw new Error(`Django response is not JSON: ${contentType || "missing content-type"}`)
  }

  return response.json() as Promise<T>
}

export function getSetCookieHeaders(response: Response) {
  const headersWithGetSetCookie = response.headers as Headers & {
    getSetCookie?: () => string[]
  }

  if (typeof headersWithGetSetCookie.getSetCookie === "function") {
    return headersWithGetSetCookie.getSetCookie()
  }

  const single = response.headers.get("set-cookie")
  return single ? [single] : []
}

function copyAllowedHeaders(
  target: Headers,
  source?: HeadersInit,
  options: { forwardAccept?: boolean } = {},
) {
  if (!source) return

  const headers = new Headers(source)
  headers.forEach((value, key) => {
    if (shouldForwardHeader(key, options)) {
      target.set(key, value)
    }
  })
}

function shouldForwardHeader(key: string, options: { forwardAccept?: boolean } = {}) {
  const lower = key.toLowerCase()

  if (lower === "accept" && !options.forwardAccept) {
    return false
  }

  return ![
    "accept-encoding",
    "connection",
    "content-length",
    "cookie",
    "host",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "set-cookie",
    "te",
    "trailer",
    "transfer-encoding",
    "upgrade",
  ].includes(lower)
}

function stripLeadingSlash(path: string) {
  return path.replace(/^\/+/, "")
}

function toSearchParams(query: DjangoQuery) {
  if (query instanceof URLSearchParams) return query

  const params = new URLSearchParams()

  for (const [key, value] of Object.entries(query)) {
    if (Array.isArray(value)) {
      for (const item of value) {
        if (item !== null && item !== undefined) params.append(key, String(item))
      }
    } else if (value !== null && value !== undefined) {
      params.set(key, String(value))
    }
  }

  return params
}

function encodeCookiePart(value: string) {
  return encodeURIComponent(value).replace(/%3A/gi, ":")
}
