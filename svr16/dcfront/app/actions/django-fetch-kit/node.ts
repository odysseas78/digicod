import {
  buildDjangoUrl,
  buildForwardHeaders,
  DjangoFetchInput,
  DjangoHttpMethod,
  readJsonOrThrow,
  serializeDjangoBody,
} from "./shared"

type NodeDjangoFetchInput = DjangoFetchInput & {
  incomingHeaders?: HeadersInit
}

export async function djangoNodeFetch(input: NodeDjangoFetchInput) {
  const method = (input.method ?? "GET").toUpperCase() as DjangoHttpMethod
  const serialized = serializeDjangoBody(method, input.body, input.bodyKind)

  return fetch(buildDjangoUrl(input), {
    method,
    headers: buildForwardHeaders({
      incomingHeaders: input.incomingHeaders,
      extraHeaders: input.headers,
      bodyHeaders: serialized.headers,
      cookieHeader: input.cookieHeader,
      authToken: input.authToken,
    }),
    body: serialized.body,
    credentials: "include",
    cache: input.cache ?? "no-store",
  })
}

export async function djangoNodeJson<T>(input: NodeDjangoFetchInput) {
  const response = await djangoNodeFetch(input)
  return readJsonOrThrow<T>(response)
}

export async function djangoNodeCommand<T>(
  command: string,
  params: unknown = {},
  options: Omit<NodeDjangoFetchInput, "path" | "method" | "query" | "body"> = {},
) {
  return djangoNodeJson<T>({
    ...options,
    method: "GET",
    path: "/api/c/",
    query: { u: command, p: JSON.stringify(params) },
  })
}
