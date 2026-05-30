"use server"
import { AvatarIcon } from '@radix-ui/react-icons';
import { cn } from '@/lib/utils';
import Cart from "@/app/checkout/cart/cart";
import CurrSel from "@/components/Currency/CurrencyDropdown";
import Link from 'next/link';
// import useWindowSize from '@/hooks/UseWindowSize'
import MenuBar from "./MyMenu";
// import fetchActionClient from "@/app/actions/fetchActionClient";
import fetchActionServer from "@/app/actions/fetchActionServer";
import wk from '@/lib/wk'
import Loading from '@/components/Loader'
import { Button } from '@/components/ui/button';
import { getRequestKind } from '@/app/lib/request-kind'
import Dialogs from '@/components/Dialogs/Dialogs'
import ViewportSetter from '@/components/ViewportSetter'
import TestButton from './TestButton'
import { Dropdown } from './DropDown'
import { WalletPopover } from './WalletPopover';
import { headers, cookies } from 'next/headers';






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



  



export default async function SiteHeader({ }) {
    const requestKind = await getRequestKind()
    const cookieStore = await cookies()
    // setTimeout(() => fetchActionServer('GetBrand', {}), 20000);
    // debounc(() => fetchActionServer('GetBrand', {}), 20000)
  
  
    const fbasket = !requestKind.isClientNavigation && await fetchActionServer('GET',"shop.cart")
    const fcategory = !requestKind.isClientNavigation && await fetchActionServer('GET','shop.category')
    const fcurrency = !requestKind.isClientNavigation && await fetchActionServer('GET','shop.currency')
  //  const fcategory = await fetchActionServer('GetCategory', {})
  const unauth = fbasket?.unauthorized || fcategory?.unauthorized  || fcurrency?.unauthorized
  // console.log(fbasket?.unauthorized || fcategory?.unauthorized  || fcurrency?.unauthorized)

  if(unauth === 401) return (
    <TestButton {...{ unauth }} />
  )
  const usr = cookieStore.get('_usr')?.value
  // console.log(usr)
  return (
    <div 
    className="border-grid sticky top-0 z-50 w-full flex bg-background/90 backdrop-blur supports-backdrop-filter:bg-background/90 shadow-md dark:shadow-md shadow-neutral-300 dark:shadow-accent/30">
      <ViewportSetter />
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
            <Link href={{pathname: "/"}} className='active:scale-95' >
              {/* <img ref={logim} src={`/logos/dcicon.png`} className={cn('h-[30px] min-w-[30px] scale-0 sm:hidden absolute dark:relative dark:scale-100 pointer-events-none' )} alt='logo' />
              <img ref={logim} src={`/logos/dcicon_b.webp`} className={cn('h-[30px] min-w-[30px] scale-100 dark:scale-0 dark:absolute sm:hidden pointer-events-none' )} alt='logo' />
              <img ref={logim2} src={`/logos/dclast.png`} className={cn('h-8 hidden sm:block scale-0 absolute dark:relative dark:scale-100 pointer-events-none')} alt='logo' />
              <img ref={logim2} src={`/logos/dclast_b.png`} className={cn('h-8 hidden sm:block scale-100 dark:scale-0 dark:absolute pointer-events-none')} alt='logo' /> */}

              <img src={`/logos/dclast_b.png`} className={cn('h-7 sm:h-8 scale-100 dark:scale-0 dark:absolute')} alt='logo' />
              <img src={`/logos/dclast.png`} className={cn('h-7 sm:h-8 scale-0 absolute dark:relative dark:scale-100')} alt='logo' />

            </Link>
          </div>
          <div className='hidden md:block' >
              <MenuBar {...{ fcategory }} />
          </div>
        </div>
        <div className="flex flex-row items-center justify-end w-[25%] gap-[20px] pr-1">
          <div className='notranslate'>
              <CurrSel {...{ fcurrency, fbasket }} /> 
          </div>
          {/* <Button onClick={(e)=>router.prefetch('http://localhost:3000/ca/giftcards/mifinity')} >dfdfdf</Button> */}
          {usr === "True" && <WalletPopover />}
          <div className='' >
            {/* <Link href={"/account"} > */}
             <Dropdown />
              
              {/* </Dropdown> */}
            {/* </Link> */}
          </div>
          
        
          <div className='' >
            {/* <Suspense fallback={null}> */}
            <Cart minicart={true}  {...{ fbasket }} />
            {/* </Suspense> */}
          </div>
        </div>
      </div>
      {/* Mobile */}
      <div className='w-full flex h-full max-h-min items-center p-3 pt-0 justify-between md:hidden'>
        <div className='' >
            <MenuBar {...{ fcategory }}  />
        </div>
      </div>
    </div>
    <Dialogs />
   </div>
  )
}

