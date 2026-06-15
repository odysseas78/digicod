# Django fetch kit

Neue, isolierte Fetch-Varianten fuer Next.js Server Actions, Next.js Route Handler und reine Node-Prozesse.

Der wichtigste Fix gegen `RequestContentLengthMismatchError` ist: `content-length` wird nie vom Browser-Request weitergeleitet und der Body wird vor `fetch` eindeutig serialisiert. Fuer JSON wird `JSON.stringify(body)` genutzt, fuer `FormData` wird kein eigener `content-type` gesetzt, und `GET`/`HEAD` senden keinen Body.

## Next.js Server Action

```ts
"use server"

import { djangoCommand, djangoGet, djangoPostJson } from "@/app/actions/django-fetch-kit/next-server"

export async function getBasket(filters = {}) {
  return djangoCommand("GetBasket", filters)
}

export async function getMe() {
  return djangoGet("/rest/me/")
}

export async function addToCart(payload: unknown, fingerprint?: string) {
  return djangoPostJson("/cart/add/", payload, {
    browserFingerprint: fingerprint,
  })
}
```

## Next.js Route Handler Proxy

```ts
import { NextRequest } from "next/server"
import { proxyNextRequestToDjango } from "@/app/actions/django-fetch-kit/route-handler"

export async function POST(request: NextRequest) {
  return proxyNextRequestToDjango({
    request,
    path: "/api/cart/add/",
  })
}
```

## Node

```ts
import { djangoNodeCommand, djangoNodeJson } from "@/app/actions/django-fetch-kit/node"

const basket = await djangoNodeCommand("GetBasket", {}, {
  cookieHeader: "auth_token=...",
})

const result = await djangoNodeJson({
  method: "POST",
  path: "/api/cart/add/",
  body: { product_id: 123, quantity: 1 },
  authToken: "...",
})
```

## Django-kompatible Body-Varianten

```ts
await djangoPostJson("/json/", { a: 1 })

await djangoJson({
  method: "POST",
  path: "/api/form/",
  body: { a: 1 },
  bodyKind: "urlencoded",
})

await djangoJson({
  method: "POST",
  path: "/api/upload/",
  body: formData,
})
```

Setze optional `DJANGO_INTERNAL_URL` oder `DJANGO_API_URL`. Ohne Env-Fallback wird `https://front.digicod.eu` verwendet.
