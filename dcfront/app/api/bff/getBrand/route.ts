// src/app/api/bff/getBrand/route.ts
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
  const searchParams = request.nextUrl.searchParams
  const filter = searchParams.get('filter') || 'giftcards'

  const prms = {
    u: 'GetBrand',
    p: JSON.stringify({ filter }),
  }

  const urlParams = new URLSearchParams(prms)

  const { headers } = await buildForwardHeaders(request)

  const upstream = await fetch(djangoUrl(`/c/?${urlParams.toString()}`), {
    method: 'GET',
    headers,
    cache: 'no-store',
  })

  const response = new NextResponse(upstream.body, {
    status: upstream.status,
    statusText: upstream.statusText,
  })

  copyHeaders(upstream, response)
  syncUpstreamCookies(upstream, response)

  return response
}