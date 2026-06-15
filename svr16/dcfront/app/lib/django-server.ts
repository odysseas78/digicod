// // src/lib/django-server.ts
// import 'server-only'
// import { cookies, headers as Hdrs } from 'next/headers'
// import { buildCookieHeader, buildDjangoUrl } from '@/app/lib/django-shared'

// type DjangoServerFetchInit = RequestInit

// export async function djangoServerFetch(
//   pathWithQuery: string,
//   init: DjangoServerFetchInit = {}
// ) {
//   const cookieStore = await cookies()
//   const sessionid = cookieStore.get('sessionid')?.value
//   const csrftoken = cookieStore.get('csrftoken')?.value

//   const headers = new Headers(init.headers)

//   if (!headers.has('accept')) {
//     headers.set('accept', 'application/json')
//   }

//   const method = (init.method ?? 'GET').toUpperCase()

//   if (
//     !headers.has('content-type') &&
//     init.body &&
//     !(init.body instanceof FormData)
//   ) {
//     headers.set('content-type', 'application/json')
//   }

//   const cookieHeader = buildCookieHeader({ sessionid, csrftoken })
//   if (cookieHeader) {
//     headers.set('cookie', cookieHeader)
//   }

//   if (!['GET', 'HEAD', 'OPTIONS', 'TRACE'].includes(method) && csrftoken) {
//     headers.set('x-csrftoken', csrftoken)
//   }

//   if (process.env.APP_ORIGIN) {
//     headers.set('origin', process.env.APP_ORIGIN)
//     headers.set('referer', `${process.env.APP_ORIGIN}/`)
//   }

//   const headerStore = await Hdrs();

//   const token = cookieStore.get("auth_token")?.value
//   headerStore.forEach((v,k)=>{
//       k !== 'accept' && headers.append(k, v)
//      })
//      headers.append("Authorization", token ? `Token ${token}` : "")

//     // console.log(headers);
    
//   return fetch(buildDjangoUrl(pathWithQuery), {
//     ...init,
//     method:method,
//     headers:headers,
//     cache: init.cache ?? 'no-store',
//   })
// }