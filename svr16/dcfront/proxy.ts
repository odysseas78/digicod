// src/middleware.ts
import { NextRequest, NextResponse } from 'next/server'
import { NavigationEvents } from '@/components/navigation-events'
import { cookies, headers } from "next/headers";

const protectedRoutes = ['/account', '/checkout?c=sendorder']

function isProtected(pathname: string) {
  return protectedRoutes.some((route) => pathname.startsWith(route))
}

export async function proxy(request: NextRequest, hhhh: any) {
    const cookieStore = await cookies()
  const headersStore = await headers()
  const authcheck = (request.cookies.get('auth_token')?.value && request.cookies.get('_usr')?.value === "True") ? true: false

  // console.log(authcheck)


  cookieStore.set('usr_' , `${authcheck}`)
    // `${request.cookies.get('resp')?.value}`,  
  // `${request.cookies.get('test')?.value}`,
  // request.cookies.get('_polz')?.value);
// request.cookies.get('hhhh') && request.cookies.delete('hhhh')
  // console.log('hhhhhh',  );
  // !request.cookies.get('kkkkkk') && request.cookies.set('kkkkkk', 'uuuuuuuu')
  // console.log('request.Url', cookieStore.get('_usr'));
  // console.log('request headers', request.headers);
  // console.log('x-forwarded-for', headersStore.get('Authorization'));
  
  const { pathname, searchParams, search } = request.nextUrl
  // const sessionid = request.cookies.get('sessionid')?.value
// console.log("pathname: ",pathname+(search ? search: ""));
  if (isProtected(pathname+(search ? search: "")) && !authcheck) {
    const loginUrl = new URL('/login', request.url)
    // loginUrl.searchParams.set('next', pathname)
    return NextResponse.redirect(loginUrl)
  }

  if (pathname === '/login' && authcheck) {
    return NextResponse.redirect(new URL('/account', request.url))
  }

  const response = NextResponse.next()
  
  return response
}

export const config = {
  matcher: ['/:path*', '/account/:path*']
}