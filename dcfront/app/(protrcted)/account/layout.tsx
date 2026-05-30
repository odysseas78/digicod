import { cookies, headers } from "next/headers";
import { redirect } from 'next/navigation'
import { ReactNode } from 'react';


export default async function AccountLayout({ children }: { children: ReactNode }) {
  // 'use client';
  // const client = await createClient({url: 'redis://localhost:6666/1'})
  // .on('error', err => console.log('Redis Client Error', err))
  // .connect();

  // const ff = await client.del('foo');
  // console.log(ff)
  const cookieStore = await cookies()
  // await new Promise(resolve => setTimeout(resolve, 5000));
  // console.log(cookieStore.get('_usr')?.value);
  // if(cookieStore.get('_usr')?.value !== 'True') return redirect("/login")

  return (
    <>
      {children}
    </>
  );
}
