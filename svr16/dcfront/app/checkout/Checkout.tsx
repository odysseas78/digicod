//@ts-nocheck
"use client"
// export const dynamic = "force-dynamic";
import dynamic from 'next/dynamic';
import { Suspense } from 'react';
import fetchActionClient from '@/app/actions/fetchActionBrowser'
import Cart from '@/app/checkout/cart/cart';
import { initFingerprint } from '@/app/checkout/helpers/functions';
import {
    ResizableHandle,
    ResizablePanel,
    ResizablePanelGroup,
} from "@/components/ui/resizable";
import wk from '@/lib/wk';
import { useRouter, useParams, usePathname, useSearchParams } from "next/navigation";
import { useEffect, useRef, useState } from 'react';
import { defStore, simpleStore } from '@/store/zustand_1';
import {
    Collapsible,
    CollapsibleContent,
    CollapsibleTrigger,
  } from "@/components/ui/collapsible"
import SendOrder from '@/app/checkout/sendorder'
import Loading from './loading'


function setCookie(name, value, days = 365) {
    const expires = new Date(Date.now() + days * 864e5).toUTCString();
    document.cookie = `${name}=${value}; expires=${expires}; path=/; SameSite=Lax`;
}
// function getCookie(name=null) {
//     if (typeof document === 'undefined') return null;
//     if(!name) return document.cookie;
//       return document.cookie.split('; ').find(row => row.startsWith(name + '='))?.split('=')[1]
//   }

const aa = wk.signal(0)



const useAdd = (el) => {
    const resizeObserver = new ResizeObserver((entries) => {

        aa.value = entries[0]
    });

    resizeObserver.observe(el)

}


export default function Checkout({  }) {
    "use client"
    const searchparams = useSearchParams()
    const c = searchparams.get('c')
    const oid = searchparams.get('oid')
    // const [sendorder, setSendorder] = useState(false)
    const store = defStore()
    const simste = simpleStore()
    const [collapse, setCollapse] = useState(false)
    const router = useRouter()
    const itemsref = useRef(null)
    const itemsref2 = useRef(null)
    const currency = simste.pget(["cart"])?.currency
    const pathname = usePathname()
    const loading = simste.pget(['basketloader'])
    const [IsClient, setIsClient] = useState(false)

  useEffect(() => {
   setIsClient(true)
}, [])

    // typeof document !== 'undefined' && simste.pget(["cart"])?.id && setCookie('_ccc', simste.pget(["cart"])?.id)
    // initFingerprint()

    useEffect(()=>{
        // simste.pget(["cart"])?.id && setCookie('_ccc', simste.pget(["cart"])?.id)
        // initFingerprint()
        if(oid){
            if(c === "ok"){
            setTimeout(async () =>{
                const res = await fetchActionClient("OrderSend", {oid:oid})
                console.log(res)
                },300)
            } 
        }
    },[])

      // ###############################
  useEffect(() => {
    
    const id = setTimeout(() => {
   
     
    }, 0)
    return () => {clearTimeout(id)} 
  }, [])
  // ###############################
    useEffect(() => {
        if (simste.pget(["cart"])?.total_products && !(simste.pget(["cart"])?.total_products > 0)) {

            // console.log(simste.pget(["cart"])?.total_products)
            return router.push("/"); // Leite zu einer anderen Seite um
        }
    
    }, [simste.pget(["cart"])?.total_products]);
    

    return (
IsClient?
        <div className='w-full px-px h-full mt-px' >
        
            {(store.sendorder && c === 'sendorder') ? <SendOrder {...{store, simste, router, searchparams}} />:
            <div className='w-full sm:w-2/3 md:w-2/3 lg:w-1/2 m-auto'>
                {/* <Suspense> */}
                    {/* <Cart basketdata={basketdata} pathname={pathname}  /> */}
                    <Cart pathname={pathname}  />
                {/* </Suspense> */}
                
            </div>}
        </div>
        :
        <Loading />
    )


}







