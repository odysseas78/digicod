// src/app/api/bff/login/route.ts
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
  const body = await request.text()
  const { headers } = await buildForwardHeaders(request)

  headers.set('content-type', 'application/json')

  const upstream = await fetch(djangoUrl('/rest/login/'), {
    method: 'POST',
    headers,
    body,
    cache: 'no-store',
    redirect: 'manual',
  })

  const response = new NextResponse(upstream.body, {
    status: upstream.status,
    statusText: upstream.statusText,
  })

  copyHeaders(upstream, response)
  syncUpstreamCookies(upstream, response)

  return response
}