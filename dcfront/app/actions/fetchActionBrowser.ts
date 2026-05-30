"use client"

import fetchActionClient from "@/app/actions/fetchActionClient"
import { getBrowserFingerprint } from "@/app/lib/fingerprint-client"

export default async function fetchActionBrowser(type:any, path:any, data:any) {
  const fingerprint = await getBrowserFingerprint()
  return fetchActionClient(type, path, data, fingerprint)
}
