"use client"

import { useEffect } from "react"

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    const payload = {
      type: "next.global-error",
      message: error?.message || "Unknown global error",
      stack: error?.stack || null,
      digest: error?.digest || null,
      url: window.location.href,
      userAgent: navigator.userAgent,
      timestamp: new Date().toISOString(),
    }

    fetch("/client-error", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
      keepalive: true,
    }).catch(() => {})
  }, [error])

  return (
    <html lang="en">
      <body className="min-h-screen bg-white text-black">
        <div className="mx-auto flex min-h-screen max-w-[720px] flex-col items-start justify-center gap-4 px-6">
          <h1 className="text-2xl font-semibold">Application error</h1>
          <p className="text-sm text-neutral-700">
            A client-side error occurred. Please try reloading the page.
          </p>
          <button
            type="button"
            onClick={() => reset()}
            className="rounded-md border border-black px-4 py-2 text-sm"
          >
            Try again
          </button>
          {process.env.NODE_ENV !== "production" && error?.message ? (
            <pre className="max-w-full overflow-auto text-xs text-red-700">
              {error.message}
            </pre>
          ) : null}
        </div>
      </body>
    </html>
  )
}
