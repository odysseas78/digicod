//@ts-nocheck
// 'use client';
// export const dynamic = "force-dynamic";
// import dynamic from 'next/dynamic';
// import DrawerManager from '@/components/Drawer/DrawerManager';
// const DrawerManager = dynamic(() => import('@/components/Drawer/DrawerManager'), {
//     ssr: false,
//   });




export default async function LoginCheckLayout({ children }) {
  // 'use client';


  return (
    <>
      {children}
    </>
  );
}
