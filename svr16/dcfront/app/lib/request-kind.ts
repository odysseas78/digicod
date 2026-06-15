import { headers } from 'next/headers'

export type RequestKind = {
  isClientNavigation: boolean
  isDocumentRequest: boolean
  isLikelyReload: boolean
  referer: string | null
  secFetchDest: string | null
  secFetchMode: string | null
}

export async function getRequestKind(): Promise<RequestKind> {
  const headerStore = await headers()

  const accept = headerStore.get('accept') || ''
  const rsc = headerStore.get('rsc')
  const nextUrl = headerStore.get('next-url')
  const secFetchDest = headerStore.get('sec-fetch-dest')
  const secFetchMode = headerStore.get('sec-fetch-mode')
  const referer = headerStore.get('referer')
  const host = headerStore.get('host')
  const proto = headerStore.get('x-forwarded-proto') || 'https'

  const currentUrl = nextUrl ? `${proto}://${host}${nextUrl}` : null

  const isClientNavigation =
    rsc === '1' ||
    accept.includes('text/x-component')

  const isDocumentRequest =
    secFetchDest === 'document' &&
    secFetchMode === 'navigate' &&
    !isClientNavigation

  // Reload ist serverseitig nicht sicher erkennbar.
  // Diese Heuristik trifft vor allem echte Browser-Reloads derselben URL.
  const isLikelyReload =
    isDocumentRequest &&
    !!referer &&
    !!currentUrl &&
    referer === currentUrl

  return {
    isClientNavigation,
    isDocumentRequest,
    isLikelyReload,
    referer,
    secFetchDest,
    secFetchMode,
  }
}
