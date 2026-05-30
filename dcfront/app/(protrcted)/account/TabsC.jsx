"use client";
import {
   Tabs,
   TabsContent,
   TabsContents,
   TabsList,
   TabsTrigger,
 } from '@/components/animate-ui/components/radix/tabs';
 import {
   Card,
   CardContent,
   CardDescription,
   CardFooter,
   CardHeader,
   CardTitle,
 } from '@/components/ui/card';
import { useParams, usePathname, useRouter, useSearchParams } from "next/navigation";
import { useEffect, useState, useRef } from 'react'
import CoinWallet from '@/app/(protrcted)/account/CoinWallet/CoinWallet'
import Orders from '@/app/(protrcted)/account/Orders/Orders'
import StartPage from '@/app/(protrcted)/account/Startpage/StartPage'
import { simpleStore } from '@/store/zustand_1';
import { WalletBallance } from '@/app/(protrcted)/account/CoinWallet/CoinWallet';


const dateFormat = (date, dateonly="")=>{
   const doptions = {
     year: "2-digit",
     month:"2-digit",
     day:"2-digit",
     }
     const toptions = {
       hour12 : false,
       hour:  "2-digit",
       minute: "2-digit",
     }
     //@ts-ignore
   const dres = new Date(date).toLocaleDateString("de-DE", doptions);
   //@ts-ignore
   const tres = new Date(date).toLocaleTimeString("de-DE", toptions);
   
   if(dateonly === "dateonly"){
     return (`${dres}`)
   } else {
     return (`${dres} ${tres}`)
   }
 }


// typeof document !== 'undefined' && document.addEventListener("touchstart", (event) => {console.log(event) })

 
export default function TabsC({}){
   const simste = simpleStore()
   const [IsClient, setIsClient] = useState(false)
   const tabvalues = ["orders", "wallet", "profile"]
   const searchparams = useSearchParams()
   const pathname = usePathname()
   const router = useRouter()
   const termsref = useRef()
   const cb = searchparams.get('c')
   const filtred = (tabvalues.filter((f)=>f===cb)[0] || tabvalues.filter((f)=>f==="profile")[0])
   const c = filtred
   const [tabsval, setTabsval] = useState(c)
   useEffect(()=>{
      setTabsval(c)
   },[c, searchparams])
   
   useEffect(() => {
      setIsClient(true)

    }, [])
    const account_loading = simste.pget(["account_loading"]) 
    
   return (
      IsClient && 
      <Tabs 
         defaultValue={tabsval} 
         value={tabsval} 
         onValueChange={(e)=> {
            router.push('/account?c='+e)
         setTabsval(e)
         
         } } 
         className="w-full max-w-[600px] m-auto p-1 rounded-md text-center relative">
            {tabsval === "wallet" && <div className='absolute top-[-9px] right-[3px]' ><WalletBallance /></div>}
         <TabsList className='text-xs!' >
            <TabsTrigger className='text-xs! sm:text-sm!' disabled={account_loading} value="orders">Orders</TabsTrigger>
            <TabsTrigger className='text-xs! sm:text-sm!' disabled={account_loading} value="wallet">Wallet</TabsTrigger>
            <TabsTrigger className='text-xs! sm:text-sm!' disabled={account_loading} value="profile">Profile</TabsTrigger>
         </TabsList>
         
         <Card className="px-0! py-[10px] m-0! w-full relative">
            <TabsContents>
               <TabsContent className="p-1" value="orders">
                  <Orders {...{}} />
               </TabsContent>
               <TabsContent value="wallet">
                  <CoinWallet {...{}} />
               </TabsContent>
               <TabsContent className='px-[10px]!' value="profile">
                  <StartPage />
               </TabsContent>
            </TabsContents>
         </Card>
      </Tabs>
   )
}

function ClsListToggle(el, clsList) {
   
   for (const cls of clsList){
      el?.classList.toggle(cls)
   }
}




