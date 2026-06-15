// src/app/api/bff/me/route.ts
import { NextRequest, NextResponse } from 'next/server'
import {
  buildForwardHeaders,
  copyHeaders,
  djangoUrl,
  syncUpstreamCookies,
} from '@/app/lib/django'

export const runtime = 'nodejs'
export const dynamic = 'force-dynamic'

export async function GET(request: NextRequest) {
  const { headers } = await buildForwardHeaders(request)

  const upstream = await fetch(djangoUrl('/rest/me/'), {
    method: 'GET',
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

  return response
}