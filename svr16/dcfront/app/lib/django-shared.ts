// // src/lib/django-shared.ts
// import { NextResponse } from 'next/server'

// type SameSite = 'lax' | 'strict' | 'none'

// type ParsedCookie = {
//   name: string
//   value: string
//   path?: string
//   maxAge?: number
//   expires?: Date
//   sameSite?: SameSite
//   secure?: boolean
//   httpOnly?: boolean
// }

// export function buildDjangoUrl(pathWithQuery: string) {
//   const base = process.env.DJANGO_INTERNAL_URL
//   if (!base) {
//     throw new Error('DJANGO_INTERNAL_URL fehlt')
//   }
//   const normalizedBase = base.endsWith('/') ? base : `${base}/`
//   return new URL(pathWithQuery, normalizedBase).toString()
// }

// export function buildCookieHeader(values: Record<string, string | undefined>) {
//   return Object.entries(values)
//     .filter(([, value]) => value)
//     .map(([name, value]) => `${name}=${value}`)
//     .join('; ')
// }

// export function methodHasBody(method: string) {
//   const upper = method.toUpperCase()
//   return !['GET', 'HEAD'].includes(upper)
// }

// function parseSetCookie(setCookie: string): ParsedCookie | null {
//   const parts = setCookie.split(';').map((part) => part.trim())
//   const [nameValue, ...attrs] = parts

//   const eqIndex = nameValue.indexOf('=')
//   if (eqIndex === -1) return null

//   const cookie: ParsedCookie = {
//     name: nameValue.slice(0, eqIndex),
//     value: nameValue.slice(eqIndex + 1),
//     path: '/',
//   }

//   for (const attr of attrs) {
//     const [rawKey, ...rawValueParts] = attr.split('=')
//     const key = rawKey.toLowerCase()
//     const rawValue = rawValueParts.join('=')

//     if (key === 'path') cookie.path = rawValue || '/'
//     else if (key === 'max-age') {
//       const n = Number(rawValue)
//       if (Number.isFinite(n)) cookie.maxAge = n
//     } else if (key === 'expires') {
//       const d = new Date(rawValue)
//       if (!Number.isNaN(d.getTime())) cookie.expires = d
//     } else if (key === 'samesite') {
//       const s = rawValue.toLowerCase()
//       if (s === 'lax' || s === 'strict' || s === 'none') {
//         cookie.sameSite = s
//       }
//     } else if (key === 'secure') cookie.secure = true
//     else if (key === 'httponly') cookie.httpOnly = true
//   }

//   return cookie
// }

// export function copySafeResponseHeaders(upstream: Response, response: NextResponse) {
//   const skip = new Set([
//     'connection',
//     'keep-alive',
//     'proxy-authenticate',
//     'proxy-authorization',
//     'te',
//     'trailers',
//     'transfer-encoding',
//     'upgrade',
//     'set-cookie',
//   ])

//   upstream.headers.forEach((value, key) => {
//     if (!skip.has(key.toLowerCase())) {
//       response.headers.set(key, value)
//     }
//   })
// }

// export function syncUpstreamCookies(upstream: Response, response: NextResponse) {
//   for (const raw of upstream.headers.getSetCookie()) {
//     const parsed = parseSetCookie(raw)
//     if (!parsed) continue

//     response.cookies.set({
//       name: parsed.name,
//       value: parsed.value,
//       path: parsed.path ?? '/',
//       httpOnly: parsed.httpOnly ?? true,
//       secure: parsed.secure ?? process.env.NODE_ENV === 'production',
//       sameSite: parsed.sameSite ?? 'lax',
//       ...(parsed.maxAge !== undefined ? { maxAge: parsed.maxAge } : {}),
//       ...(parsed.expires ? { expires: parsed.expires } : {}),
//     })
//   }
// }