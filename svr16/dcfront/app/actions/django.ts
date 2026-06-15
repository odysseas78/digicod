// src/lib/django.ts
import { cookies } from 'next/headers'
import { NextRequest, NextResponse } from 'next/server'

type SameSite = 'lax' | 'strict' | 'none'

type ParsedCookie = {
  name: string
  value: string
  path?: string
  maxAge?: number
  expires?: Date
  secure?: boolean
  httpOnly?: boolean
  sameSite?: SameSite
}

export function djangoUrl(path: string) {
  const base = process.env.DJANGO_INTERNAL_URL
  if (!base) {
    throw new Error('DJANGO_INTERNAL_URL fehlt')
  }

  const normalizedBase = base.endsWith('/') ? base.slice(0, -1) : base
  const normalizedPath = path.startsWith('/') ? path : `/${path}`

  return `${normalizedBase}${normalizedPath}`
}

export async function buildForwardHeaders(request?: NextRequest) {
  const cookieStore = await cookies()
  const sessionid = cookieStore.get('sessionid')?.value
  const csrftoken = cookieStore.get('csrftoken')?.value

  const headers = new Headers()

  headers.set('accept', 'application/json')

  if (process.env.APP_ORIGIN) {
    headers.set('origin', process.env.APP_ORIGIN)
    headers.set('referer', `${process.env.APP_ORIGIN}/`)
  }

  const cookieParts: string[] = []
  if (sessionid) cookieParts.push(`sessionid=${sessionid}`)
  if (csrftoken) cookieParts.push(`csrftoken=${csrftoken}`)

  if (cookieParts.length > 0) {
    headers.set('cookie', cookieParts.join('; '))
  }

  if (request) {
    const host = request.headers.get('host')
    const userAgent = request.headers.get('user-agent')
    const ip =
      request.headers.get('x-forwarded-for') ||
      request.headers.get('x-real-ip') ||
      ''

    if (host) headers.set('x-forwarded-host', host)
    if (userAgent) headers.set('user-agent', userAgent)
    if (ip) headers.set('x-forwarded-for', ip)

    headers.set(
      'x-forwarded-proto',
      request.nextUrl.protocol.replace(':', '')
    )
  }

  return { headers, sessionid, csrftoken }
}

function parseSetCookie(raw: string): ParsedCookie | null {
  const parts = raw.split(';').map((p) => p.trim())
  const [nameValue, ...attrs] = parts

  const eq = nameValue.indexOf('=')
  if (eq === -1) return null

  const cookie: ParsedCookie = {
    name: nameValue.slice(0, eq),
    value: nameValue.slice(eq + 1),
    path: '/',
  }

  for (const attr of attrs) {
    const [k, ...rest] = attr.split('=')
    const key = k.toLowerCase()
    const value = rest.join('=')

    if (key === 'path') cookie.path = value || '/'
    else if (key === 'max-age') {
      const n = Number(value)
      if (Number.isFinite(n)) cookie.maxAge = n
    } else if (key === 'expires') {
      const d = new Date(value)
      if (!Number.isNaN(d.getTime())) cookie.expires = d
    } else if (key === 'secure') cookie.secure = true
    else if (key === 'httponly') cookie.httpOnly = true
    else if (key === 'samesite') {
      const s = value.toLowerCase()
      if (s === 'lax' || s === 'strict' || s === 'none') {
        cookie.sameSite = s
      }
    }
  }

  return cookie
}

export function syncUpstreamCookies(
  upstream: Response,
  response: NextResponse
) {
  for (const raw of upstream.headers.getSetCookie()) {
    const parsed = parseSetCookie(raw)
    if (!parsed) continue

    response.cookies.set({
      name: parsed.name,
      value: parsed.value,
      path: parsed.path ?? '/',
      httpOnly: parsed.httpOnly ?? true,
      secure: parsed.secure ?? process.env.NODE_ENV === 'production',
      sameSite: parsed.sameSite ?? 'lax',
      ...(parsed.maxAge !== undefined ? { maxAge: parsed.maxAge } : {}),
      ...(parsed.expires ? { expires: parsed.expires } : {}),
    })
  }
}

export function copyHeaders(upstream: Response, response: NextResponse) {
  const skip = new Set([
    'set-cookie',
    'content-length',
    'transfer-encoding',
    'connection',
  ])

  upstream.headers.forEach((value, key) => {
    if (!skip.has(key.toLowerCase())) {
      response.headers.set(key, value)
    }
  })
}