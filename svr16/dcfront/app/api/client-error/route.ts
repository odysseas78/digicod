import { NextRequest, NextResponse } from "next/server"

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()

    console.error("[client-error]", {
      type: body?.type || "unknown",
      message: body?.message || "Unknown error",
      source: body?.source || null,
      line: body?.line || null,
      column: body?.column || null,
      stack: body?.stack || null,
      details: body?.details || null,
      url: body?.url || null,
      viewport: body?.viewport || null,
      timestamp: body?.timestamp || null,
      userAgent: body?.userAgent || request.headers.get("user-agent"),
      requestIp:
        request.headers.get("x-forwarded-for") ||
        request.headers.get("x-real-ip") ||
        null,
    })

    return NextResponse.json({ ok: true })
  } catch (error) {
    console.error("[client-error][logging-failed]", error)
    return NextResponse.json({ ok: false }, { status: 400 })
  }
}
