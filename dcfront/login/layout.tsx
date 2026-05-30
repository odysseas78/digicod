//@ts-nocheck
// 'use client';
// export const dynamic = "force-dynamic";
// import dynamic from 'next/dynamic';
// import DrawerManager from '@/components/Drawer/DrawerManager';
// const DrawerManager = dynamic(() => import('@/components/Drawer/DrawerManager'), {
//     ssr: false,
//   });
// import { createClient } from 'redis';

import { cookies, headers } from "next/headers";
import { redirect } from 'next/navigation'
import LoginPage from "./page";


export default async function LoginLayout({ children }) {
  // 'use client';
  // const client = await createClient({url: 'redis://localhost:6666/1'})
  // .on('error', err => console.log('Redis Client Error', err))
  // .connect();

  // const ff = await client.del('foo');
  // console.log(ff)
  const cookieStore = await cookies()
  // await new Promise(resolve => setTimeout(resolve, 5000)); s
  // console.log("LoginPage props:", formdata);
 
  // if(cookieStore.get('auth_token')?.value) return redirect("/account")

  return (
    <>
      {children}
    </>
  );
}
