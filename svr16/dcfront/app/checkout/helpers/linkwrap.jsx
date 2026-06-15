// "use client"
//  import { defStore, simpleStore } from '@/store/zustand_1';
//  import Link from 'next/link';
// import { useParams, usePathname, useRouter, useSearchParams } from "next/navigation";
// import React, { useRef } from 'react';
// import { cn } from '@/lib/utils';






//  export const LinkWrap = ({ children, p }) =>{
//       const pathname = usePathname()
//       const store = defStore()
//       const simste = simpleStore()
//    //  const cart = mergeUniqueKeys(structuredClone(simste.pget(["cart"])), basketdata?.cart)
//       const cart = simste.pget(["cart"]).id ? simste.pget(["cart"]) : basketdata?.cart
//       const router = useRouter()
//       const fref = useRef()
//       const params = useParams()
//       const searchparams = useSearchParams()

//       return (
//          <div className='w-full text-wrap' >
//             <Link
//                replace={false}
//                scroll={false}
//                href={{
//                   pathname:`/${p.region}/${p.brand.category[0].slug}/${p.brand.slug}` }}
//                   onNavigate={(e) => {
//                      e.preventDefault()
//                   }}
//                   // className='cursor-pointer'
//                   onPointerDown={(e) => {
//                   if(e.button === 0){
//                      e.target.style.scale = 1.05
//                   }
//                }}
//                onPointerUp={(e) => {
//                   if(e.button === 0){
//                      e.target.style.scale = 1.0
//                      router.push(`/${p.region}/${p.brand.category[0].slug}/${p.brand.slug}`)
                     
//                   } 
//                }}
//                className={cn(((p.brand.slug !== params.brandslug) || ((p.brand.slug === params.brandslug) && (p.region !== store.region[0]))) ?
//                   'flex underline w-max' : 'pointer-events-none')}  >
//                {children}
//             </Link>
//          </div>
//       )
//    }