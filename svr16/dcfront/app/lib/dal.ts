// // src/lib/dal.ts
// import { djangoServerFetch } from '@/app/lib/django-server'

// export async function djangoCommand<T>(u: string, p: unknown = {}) {
//   const search = new URLSearchParams({
//     u,
//     p: JSON.stringify(p),
//   })

//   const res = await djangoServerFetch(`/c/?${search.toString()}`)

//   if (!res.ok) {
//     throw new Error(`Django command ${u} fehlgeschlagen: ${res.status}`)
//   }

//   return res.json() as Promise<T>
// }

// export function getBasket<T = unknown>(filters: unknown = {}) {
//   return djangoCommand<T>('GetBasket', filters)
// }

// export function getBrand<T = unknown>(filters = {}) {
//   return djangoCommand<T>('GetBrand', filters)
// }

// export function getProducts<T = unknown>(filters: unknown = {}) {
//   return djangoCommand<T>('GetProducts', filters)
// }

// // export function getCategory<T = unknown>(filters: unknown = {}) {
// //   return djangoCommand<T>('GetCategory', filters)
// // }

// export async function getMe<T = unknown>() {
//   const res = await djangoServerFetch('/rest/me/')

//   if (res.status === 401) return null
//   if (!res.ok) {
//     throw new Error(`getMe fehlgeschlagen: ${res.status}`)
//   }

//   return res.json() as Promise<T>
// }