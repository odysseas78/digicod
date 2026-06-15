// // src/lib/auth-client.ts
// export async function login(email: string, password: string) {
//    const res = await fetch('/api/bff/login', {
//      method: 'POST',
//      headers: {
//        'Content-Type': 'application/json',
//      },
//      body: JSON.stringify({ email, password }),
//      credentials: 'same-origin',
//    })
 
//    if (!res.ok) {
//      throw new Error(`Login fehlgeschlagen: ${res.status}`)
//    }
 
//    return res.json()
//  }
 
//  export async function logout() {
//    const res = await fetch('/api/bff/logout', {
//      method: 'POST',
//      credentials: 'same-origin',
//    })
 
//    if (!res.ok) {
//      throw new Error(`Logout fehlgeschlagen: ${res.status}`)
//    }
 
//    return res.json()
//  }
 
//  export async function getMe() {
//    const res = await fetch('/api/bff/me', {
//      method: 'GET',
//      credentials: 'same-origin',
//      cache: 'no-store',
//    })
 
//    if (res.status === 401) return null
//    if (!res.ok) {
//      throw new Error(`getMe fehlgeschlagen: ${res.status}`)
//    }
 
//    return res.json()
//  }