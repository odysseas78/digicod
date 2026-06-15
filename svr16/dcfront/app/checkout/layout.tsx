//@ts-nocheck
import { Suspense } from "react";
// 'use client';
// export const dynamic = "force-dynamic";
// import dynamic from 'next/dynamic';
// import DrawerManager from '@/components/Drawer/DrawerManager';
// const DrawerManager = dynamic(() => import('@/components/Drawer/DrawerManager'), {
//     ssr: false,
//   });
// import { createClient } from 'redis';



export default async function CheckoutLayout({ children }) {
  // 'use client';
  // const client = await createClient({url: 'redis://localhost:6666/1'})
  // .on('error', err => console.log('Redis Client Error', err))
  // .connect();

  // const ff = await client.del('foo');


  return (
    <>
      
      {/* <Suspense fallback={<div className='z-50'>Loading...</div>} > */}
          {children}
          {/* </Suspense > */}
    </>
  );
}
