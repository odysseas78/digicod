//@ts-nocheck
// 'use client';
// export const dynamic = "force-dynamic";
// import dynamic from 'next/dynamic';
// import ProductPage from '@/components/ProductView/ProductPage';

// import DrawerManager from '@/components/Drawer/DrawerManager';
// const DrawerManager = dynamic(() => import('@/components/Drawer/DrawerManager'), {
//     ssr: false,
//   });
// const ProductsList = dynamic(() => import('@/components/ProductList'), {
//   ssr: false,
// });
// const ProductPage = dynamic(() => import('@/components/ProductView/ProductPage'), {
//   ssr: false,
// });


//@ts-nocheck
export default async function BrandLayout({ children }) {

  // 'use client';
  // console.log('brand')
  //   const [response, loading,  error, axiosGet] = useAxiosFunction('GetProduct')
  //   const [load, setLoad] = useState(true)
  //     const pathname = usePathname();
  //     const router = useRouter();
  //     const params = useParams();
  //     const { catslug, brandslug, prodslug, state } = params;
  //     const store = wk.defSte()
  //     const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  //     const simplestore = wk.simSte()



  return (

    <>
      {children}

    </>
  );
}
