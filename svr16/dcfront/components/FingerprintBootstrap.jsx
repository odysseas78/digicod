"use client"
import { useEffect } from "react"
import { usePathname, useSearchParams } from "next/navigation"
import syncFingerprintCookie from "@/app/actions/syncFingerprintCookie"
import { getBrowserFingerprint } from "@/app/lib/fingerprint-client"

export default function FingerprintBootstrap() {
  const pathname = usePathname()
  const searchParams = useSearchParams()

  useEffect(() => {
    let cancelled = false

    const ensureFingerprint = async () => {
      const fingerprint = await getBrowserFingerprint()
      if (!cancelled && fingerprint) {
        await syncFingerprintCookie(fingerprint)
      }
    }

    ensureFingerprint()

    
    return () => {
      cancelled = true
    }
  }, [pathname, searchParams])

  return null
}
