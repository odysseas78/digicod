"use client"
import fetchClientServer from "@/app/actions/fetchClientServer"
import { getBrowserFingerprint } from "@/app/lib/fingerprint-client"


export default async function fetchClient(type:any, path: any, data: any) {
  const fingerprint = await getBrowserFingerprint()
  return fetchClientServer(type, path, data, fingerprint)
}