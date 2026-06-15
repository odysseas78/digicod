"use client"
export const dynamic = "force-dynamic";
import { simpleStore, defStore } from '@/store/zustand_1'
import { Suspense, useRef, useState } from 'react';
import { AvatarIcon } from '@radix-ui/react-icons';
import React, { useEffect, ChangeEvent, FormEvent, use } from 'react';
import { perStore } from "@/store/zustand_1"
import { TailwindIndicator } from "../tailwind-indicator"
import { cn } from '@/lib/utils';
import Cart from "@/app/checkout/cart/cart";
import CurrSel from "@/components/Currency/CurrencyDropdown";
import Link from 'next/link';
// import useWindowSize from '@/hooks/UseWindowSize'
import MenuBar from "./MyMenu";
import { useRouter, useParams, usePathname, useSearchParams } from "next/navigation";
// import fetchActionClient from "@/app/actions/fetchActionClient";
import ViewportSetter from '@/components/ViewportSetter'
import wk from '@/lib/wk'
import Loading from '@/components/Loader'
import { initFingerprint } from '@/app/checkout/helpers/functions';
import UseVisibility from '@/hooks/useVisible'
import useContexData from '@/store/DefContext';
import { Button } from '@/components/ui/button';
import fetchActionClient from '@/app/actions/fetchActionBrowser';
import { mergeUniqueKeys } from '@/app/checkout/cart/functions'




// console.log('SiteHeader_0')
// const beforeUnloadHandler = (event) => {
//   // Recommended
//   event.preventDefault();

//   // Included for legacy support, e.g. Chrome/Edge < 119
//   event.returnValue = false;
// };

// const nameInput = document.querySelector("#name");

// document.addEventListener("input", (event) => {
//   if (event.target.value !== "") {
//     window.addEventListener("beforeunload", beforeUnloadHandler);
//   } else {
//     window.removeEventListener("beforeunload", beforeUnloadHandler);
//   }
// });
// function getCookie(name=null) {
//   if (typeof document === 'undefined') return null;
//   if(!name) return document.cookie;
//     return document.cookie.split('; ').find(row => row.startsWith(name + '='))?.split('=')[1]
// }

// const parseFromHtmlStr = (htmlStr) =>
//   new DOMParser().parseFromString(htmlStr, "text/html").body
//     .firstChild



  


export default function SiteHeader({ fbasket, fcurrency, fcategory }) {
  'use client'
  const router = useRouter()
  const pathname = usePathname()
  const searchparams = useSearchParams()
  const simste = simpleStore()
  const store = defStore()
  const pstore = perStore()
  const cb = searchparams.get('c')
  // const { data, setContData } = useContexData();
  // console.log('SiteHeader')
  
  const [IsClient, setIsClient] = useState(false)
  const [dcur, setDcur] = useState()
  const didBootstrapRef = useRef(false)

  useEffect(() => {
   setIsClient(true)
}, [])

useEffect(() => {
  if (didBootstrapRef.current) return
  didBootstrapRef.current = true
}, [])



//  console.log(CreatePortal)

  // useEffect(()=>{if(cb !== 'sendorder' && store.sendorder) store.dset(['sendorder'], false)},[cb])

  ViewportSetter()

    useEffect(() => {
        // initFingerprint()
      // setContData({cart:cart})
      // simste.pset(["cart"], basketdata.cart)
      // if(basketdata?.cart?.id === "dum") router.push(pathname)
  
    }, [])
    // ###############################

  
  const menuref = useRef(null)
  const visible = UseVisibility(menuref)
  const menuref2 = useRef(null)
  const visible2 = UseVisibility(menuref2)

  // const blurbackdrop = <div className={cn('top-0 left-0 z-50 right-0 bottom-0 absolute backdrop-blur rounded-sm bg-background/80 animate-pulse')} ></div>
  
  return (
    <div 
    className="border-grid sticky top-0 z-50 w-full flex bg-background/90 backdrop-blur supports-backdrop-filter:bg-background/90 shadow-md dark:shadow-md shadow-neutral-300 dark:shadow-accent/30">
    {/* className="border-grid sticky top-0 h-[65px] z-50 w-full bg-background/90 backdrop-blur supports-[backdrop-filter]:bg-background/90 shadow-inner shadow-neutral-300 dark:shadow-neutral-800"> */}
          {/* {!(simste.pget(["cart"])?.currency?.shortname) && blurbackdrop} */}
    <div className="h-full max-h-min items-center justify-between w-full max-w-[1200px] m-auto">
      {/* ########## TEST BUTTON ################# */}
    {/* <Button onClick={(e)=>{
          testAction(simste)
        }} >DDD</Button> */}
        {/* ######################### */}
      <div className='w-full flex h-full max-h-min p-3 items-center justify-between'>

        <div className="flex flex-row gap-3 items-center justify-start w-[75%]">
          <div className="w-max min-w-max">
            <Link 
              href={{pathname: "/"}}
              className='active:scale-95'
              onNavigate={(e) => {
                e.preventDefault()
              }}
              // className='cursor-pointer'
              onPointerDown={(e) => {
                if(e.button === 0){
                  // if(e.target.children) e.target.children[0].style.scale = 0.95
                }
              }} 
              onPointerUp={(e) => {
                if(e.button === 0){
                  // if(e.target.children) e.target.children[0].style.scale = 1
                  router.push(`/`)
                }
              }} 
              >
              {/* <img ref={logim} src={`/logos/dcicon.png`} className={cn('h-[30px] min-w-[30px] scale-0 sm:hidden absolute dark:relative dark:scale-100 pointer-events-none' )} alt='logo' />
              <img ref={logim} src={`/logos/dcicon_b.webp`} className={cn('h-[30px] min-w-[30px] scale-100 dark:scale-0 dark:absolute sm:hidden pointer-events-none' )} alt='logo' />
              <img ref={logim2} src={`/logos/dclast.png`} className={cn('h-8 hidden sm:block scale-0 absolute dark:relative dark:scale-100 pointer-events-none')} alt='logo' />
              <img ref={logim2} src={`/logos/dclast_b.png`} className={cn('h-8 hidden sm:block scale-100 dark:scale-0 dark:absolute pointer-events-none')} alt='logo' /> */}

              <img src={`/logos/dclast_b.png`} className={cn('h-7 sm:h-8 scale-100 dark:scale-0 dark:absolute pointer-events-none')} alt='logo' />
              <img src={`/logos/dclast.png`} className={cn('h-7 sm:h-8 scale-0 absolute dark:relative dark:scale-100 pointer-events-none')} alt='logo' />

            </Link>
          </div>
          <div ref={menuref} className='hidden md:block' >
              <MenuBar {...{ fcategory }} />
          </div>
        </div>
        <div className="flex flex-row items-center justify-end w-[25%] gap-3 pr-1">
          <div className=''>
              <CurrSel {...{ fcurrency, fbasket }} /> 
          </div>
          {/* <Button onClick={(e)=>router.prefetch('http://localhost:3000/ca/giftcards/mifinity')} >dfdfdf</Button> */}
          <div className='' >
            <Link 
              href={simste.pget(["usr"]) === 'True' ? "/account" : "/login"}
              onNavigate={(e) => {
                e.preventDefault()
              }}
              onPointerDown={(e) => {
                  if(e.button === 0){
                    e.target.children[0].style.scale = 0.8
                  }
              }} 
              onPointerUp={(e) => {
                  if(e.button === 0){
                    setTimeout(()=>{
                      e.target.children[0].style.scale = 1
                    },70)
                    router.push("/login")
                  }
              }} 
              >
              <div className="rounded-full shadow-inner pointer-events-none" >
                <AvatarIcon className={cn('w-[1.8rem] h-[1.8rem] rounded-full pointer-events-none', (simste.pget(["usr"]) === 'True' ? 'text-green-700 dark:text-green-500 shadow-inner shadow-neutral-300 dark:shadow-neutral-500' : ''))} />
              </div>
            </Link>
          </div>
          
        
          <div className='' >
            {/* <Suspense fallback={null}> */}
            <Cart minicart={true}  {...{ fbasket }} />
            {/* </Suspense> */}
          </div>
        </div>
      </div>
      {/* Mobile */}
      <div ref={menuref2} className='w-full flex h-full max-h-min items-center p-3 pt-0 justify-between md:hidden'>
        <div className='' >
            <MenuBar {...{ fcategory }}  />
        </div>
      </div>
    </div>
   </div>
  )
}
