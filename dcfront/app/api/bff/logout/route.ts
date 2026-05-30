// src/app/api/bff/logout/route.ts
import { NextRequest, NextResponse } from 'next/server'
import {
  buildForwardHeaders,
  copyHeaders,
  djangoUrl,
  syncUpstreamCookies,
} from '@/app/lib/django'

export const runtime = 'nodejs'
export const dynamic = 'force-dynamic'

export async function POST(request: NextRequest) {
  const { headers, csrftoken } = await buildForwardHeaders(request)

  if (csrftoken) {
    headers.set('x-csrftoken', csrftoken)
  }

  const upstream = await fetch(djangoUrl('/rest/logout/'), {
    method: 'POST',
    headers,
    cache: 'no-store',
    redirect: 'manual',
  })

  const response = new NextResponse(upstream.body, {
    status: upstream.status,
    statusText: upstream.statusText,
  })

  copyHeaders(upstream, response)
  syncUpstreamCookies(upstream, response)

  // fallback: lokal auch löschen
  response.cookies.set({
    name: 'sessionid',
    value: '',
    path: '/',
    expires: new Date(0),
  })

  response.cookies.set({
    name: 'csrftoken',
    value: '',
    path: '/',
    expires: new Date(0),
  })

  return response
}