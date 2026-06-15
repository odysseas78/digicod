// app/actions/user.ts
"use server";
import { cookies, headers } from "next/headers";
// import { redirect } from 'next/navigation'
import parseSetCookie from '@/app/lib/parseCookie';
// import { encrypt, decrypt } from '@/lib/xorCipher'
// import { syncUpstreamCookies } from '@/app/actions/django-shared'

function fingerprintCookieOptions() {
  return {
    path: "/",
    sameSite: "lax" as const,
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    maxAge: 60 * 60 * 24 * 365,
  }
}

const d:any = []

export default async function fetchActionClient(key: any, params: any, browserFingerprint?: string | null, fingerprint?: any) {
  
  const prms = { u: key, p: JSON.stringify(params) }
  const urlParams = new URLSearchParams(prms);

  const cookieStore = await cookies();

  const headerStore = await headers();

  const token = cookieStore.get("auth_token")?.value
  const currentFingerprint = cookieStore.get("_polz")?.value
  if (browserFingerprint && currentFingerprint !== browserFingerprint) {
    cookieStore.set("_polz", browserFingerprint, fingerprintCookieOptions())
  }
  // console.log("user-agent",headerStore.get('user-agent'));
  const host = 'front.digicod.eu'
  // const host = headerStore.get('host')
  /* 🔹 Cookies serialisieren */
  const cookieMap = new Map(
    cookieStore.getAll().map((cookie) => [cookie.name, cookie.value])
  )

  if (browserFingerprint) {
    cookieMap.set("_polz", browserFingerprint)
  }

  const cookieHeader = Array.from(cookieMap.entries())
    .map(([name, value]) => `${name}=${value}`)
    .join("; ");


  const forwardHeaders = new Headers();
  headerStore.forEach((v, k) => {
    // console.log(k, v);
    k !== 'accept' && forwardHeaders.append(k, v)
  })
  forwardHeaders.append("Authorization", token ? `Token ${token}` : "")
  // forwardHeaders.append("Authorization", token ? `Token ${decrypt(token, process.env.secret)}` : "")
  forwardHeaders.append("Cookie", cookieHeader)
  forwardHeaders.append("Content-Type", "application/json")
  if (browserFingerprint) {
    // forwardHeaders.append("x-browser-fingerprint", browserFingerprint)
  }

  const urldss = key === "url" && params.url ? params.url : `https://api.${host}/${key}/?${urlParams}`

  const res = await fetch(urldss, {
    method: "GET",
    headers: forwardHeaders,
    credentials: "include",
    cache: 'force-cache',
    // cache: "no-store",
    next: { revalidate: 60 }
  });
  // syncUpstreamCookies(res, )

  // console.log(" res.headers.getSetCookie(): ",  res.headers.getSetCookie())
   res.headers.getSetCookie().forEach((c: string) => {
    const cook = parseSetCookie(c);
    if (cook.name === "auth_token") cook.value = cook.value
    // AzEJMF0VLAdeAABqIhQwIFNKAHNQSAFBCQFXJAAxXRUsB15eAQ==
    // if (cook.name === "auth_token") cook.value = encrypt(cook.value, process.env.secret)
    // console.log('cook: ',cook);
  cookieStore.set(cook)
  });

  if (!res.ok) {
    if (res.status === 401) {

      // Handle unauthorized access, e.g., clear auth cookies
      cookieStore.delete("auth_token")
    
      // console.log("401 WWWWWWWWWW: ",res)
      return {"detail":"Invalid token Error: HTTP 401"}
      // redirect('/login')
    }
  }

  const contentType = res.headers.get('content-type') || ''

  if (!res.ok) {
    const text = await res.text()
    // console.log(text)
    throw new Error(`HTTP ${res.status}: ${text.slice(0, 200000)}`)
  }

  if (contentType.includes('application/json')) {
    const data = await res.json()
      // console.log(data)
    return data
  } else {
    const text = await res.text()
    console.error('Kein JSON erhalten:', text.slice(0, 30000))
    throw new Error('Response ist kein JSON')
  }
}
