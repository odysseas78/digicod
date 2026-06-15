//@ts-nocheck
// 'use client';
// export const dynamic = "force-dynamic";
// import useAxiosFunction from '@/hooks/useAxiosFunction';
// import wk from '@/lib/wk';
// // import dynamic from 'next/dynamic';
// import { useParams, usePathname, useRouter } from 'next/navigation';
// import { useEffect } from 'react';
// const DrawerManager = dynamic(() => import('@/components/Drawer/DrawerManager'), {
//   ssr: false,
// });
// const ProductsList = dynamic(() => import('@/components/ProductList'), {
//   ssr: false,
// });

//@ts-nocheck
export default async function CatslugLayout({ children }) {

  return (
    <>
      {children}
    </>
  );
}
