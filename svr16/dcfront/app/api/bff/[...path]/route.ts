// src/app/api/bff/[...path]/route.ts
import { NextRequest, NextResponse } from 'next/server'
import {
  buildForwardHeaders,
  copyHeaders,
  djangoUrl,
  syncUpstreamCookies,
} from '@/app/lib/django'

export const runtime = 'nodejs'
export const dynamic = 'force-dynamic'

async function handler(
  request: NextRequest,
  context: { params: Promise<{ path: string[] }> }
) {
  const { path } = await context.params
  const { headers, csrftoken } = await buildForwardHeaders(request)

  const method = request.method.toUpperCase()
  const search = request.nextUrl.search
  const targetPath = `/${path.join('/')}${search}`

  const contentType = request.headers.get('content-type')
  if (contentType) {
    headers.set('content-type', contentType)
  }

  if (!['GET', 'HEAD', 'OPTIONS'].includes(method) && csrftoken) {
    headers.set('x-csrftoken', csrftoken)
  }

  const body =
    method === 'GET' || method === 'HEAD'
      ? undefined
      : await request.arrayBuffer()

  const upstream = await fetch(djangoUrl(targetPath), {
    method,
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

export const GET = handler
export const POST = handler
export const PUT = handler
export const PATCH = handler
export const DELETE = handler
export const OPTIONS = handler
export const HEAD = handler
