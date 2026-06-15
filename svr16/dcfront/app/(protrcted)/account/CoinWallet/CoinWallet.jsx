"use client"
export const dynamic = "force-dynamic";
import React, { useRef, useEffect, useState } from "react";
import { Badge } from "@/components/ui/badge"
import { createPortal } from "react-dom";
import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableHead,
    TableHeader,
    TableFooter,
    TableRow,
  } from "@/components/ui/table"
import {
   Tabs,
   TabsContent,
   TabsContents,
   TabsList,
   TabsTrigger,
 } from '@/components/animate-ui/components/radix/tabs';
import { Card } from '@/components/ui/card';
import { Button } from "@/components/ui/button";
import { tableStore } from "../tablestore";
import { Thead, TRows } from "./table/table";
import { useParams, usePathname, useRouter, useSearchParams } from "next/navigation";
import { simpleStore } from "@/store/zustand_1";
import fetchActionClient from "@/app/actions/fetchActionBrowser";
import Loading from '@/app/(protrcted)/account/loading'
import { cn } from "@/lib/utils";
import {
  ArrowRight,
  ChevronsDown,
  Loader,
  MoreVertical,
  ArrowLeftRight,
  History,
  SquarePlus, Plus, Minus, Trash, Trash2
} from 'lucide-react';
import WalletDeposits from './WalletDeposit/WalletDeposits'
import { Spinner } from '@/components/ui/spinner'
import Image from 'next/image'


export function WalletBallance({ }){
  const simste = simpleStore()
  const [data, setData] = useState(undefined)
  // const [IsClient, setIsClient] = useState(false)
  const [loading, setLoading] = useState(false)
  const walletBalance = simste.pget(["walletBalance"])
  const currency = simste.pget(["cart"]).currency

  useEffect(() => {
   const id = setTimeout(async () => {

        setLoading(true)
         const data = await fetchActionClient('GetCoinWallet', {})
         if(data?.detail === "Invalid token Error: HTTP 401") window.location.reload()
         setData(data)
        data && simste.pset(["walletBalance"], data) 
        setLoading(false)
        // setTimeout(()=>{setStartloading(false)},500)
      }, 0)

    return () => {
      clearTimeout(id)
    }
}, [currency])

const dd = data || simste.pget(["walletBalance"])

  return (
    currency &&
      <div className="py-1 px-2 border rounded-md w-max flex items-center justify-between gap-[10px] relative">

        <div className="w-max flex flex-col justify-between">
         <div className='flex gap-2 justify-between items-center border-b mb-1' >
          <span className="text-[0.60rem] text-gray-400 sm:text-[0.65rem]" > Balance</span>
          <small><i className='text-[0.60rem] sm:text-[0.65rem]'>≈ {currencyFormat(dd?.balance * 250, currency?.shortname)}</i></small>
        </div>
         <div className='text-xs sm:text-xs flex items-center gap-1'>
          <Image src={'/media/payment/dccoin.webp'} className='w-[16px] sm:w-[16px] rounded-md' width={16} height={16} alt="dcoin" />
            {new Intl.NumberFormat("en-GB").format((dd?.dcbalance * 250))}
        </div>
          
        </div>

         <Button className="active:scale-95 rounded-sm" size={"icon-lg"} variant="default" >
           {/* <img src={'/media/payment/dccoin.webp'} className='w-[20px] sm:w-[20px] rounded-md' /> */}
           <SquarePlus className="w-[25px]! h-[25px]!" />
        </Button>
        <>
           {loading && <div className='absolute top-0 left-0 right-0 bottom-0 flex justify-center bg-background/96 items-center z-50 border rounded-md'>
                <Spinner className="size-5" />
            </div>}
            
        </>
      </div>
  )
}

function myQuerySelectAll(el, array=false){
  const els = typeof document !== 'undefined' ? document.querySelectorAll(el) : undefined
  return array ? Array.from(els) : els
}

function currencyFormat(amount, currency){
  const formatted = new Intl.NumberFormat("de-DE", {
    style: "currency",
    currency: currency,
  }).format(amount)
  return formatted
}


const CoinWallet = (props) => {
  const tstore = tableStore()
  const simste = simpleStore()
  const [data, setData] = useState(undefined)
  const [IsClient, setIsClient] = useState(false)
  const [loading, setLoading] = useState(false)
  const coinWallet = simste.pget(["coinWallet"])
  const currency = simste.pget(["cart"]).currency
  const searchparams = useSearchParams()
  const pathname = usePathname()
  const router = useRouter()


// useEffect(() => {
//    const id = setTimeout(async () => {

//         setLoading(true)
//          const data = await fetchActionClient('GetCoinWallet', {})
//          if(data?.detail === "Invalid token Error: HTTP 401") window.location.reload()
//          setData(data)
//         data && simste.pset(["coinWallet"], data) 
//         setLoading(false)
//         // setTimeout(()=>{setStartloading(false)},500)
//       }, 0)

//     return () => {
//       clearTimeout(id)
//     }
// }, [currency])



 
//############################################################
  // const [a, setA] = useState(false)
  // useEffect(()=>{
  //     // Table state wiederherstellen
  //     const tid = setTimeout(() => {
  //       const colaps = myQuerySelectAll('[data-colaps]')
  //       const clickrow = myQuerySelectAll('[data-clickrow]')
  //       if(!(colaps.length > 0 && tstore.wtablestate)) setA((prev)=>!prev)
  //       if(colaps.length > 0 && tstore.wtablestate){
  //         for (let i = 0; i < colaps.length; i++) {
  //           colaps[i].classList.value = tstore.wtablestate.colapsClsVal[i]
  //           clickrow[i].classList.value = tstore.wtablestate.clickrowClsVal[i]
  //         }
  //       }
  //     }, 100);
  
  //   return () => {
  //     clearTimeout(tid)
  //   }
  // },[a])
//#############################################################

useEffect(() => {
  setIsClient(true)
}, [])



const wallettabs = simste.pget(['wallettabs'])




const account_loading = simste.pget(["account_loading"]) 

  return (
    IsClient &&
    <>
    {/* <div className="border-b px-2 pb-2 mt-[-5px]" >
        <WalletBallance {...{ }} />
    </div> */}
    
     <Tabs 
         defaultValue={'transactions'} 
         value={wallettabs} 
         onValueChange={(e)=> {
          router.push('/account?c=wallet&b='+e)
          // e === "history" && router.push('/account?c=wallet&b='+e)
          e === "transactions" && router.refresh()
         simste.pset(['wallettabs'], e)
        //  console.log(wallettabs)
         
         } } 
         className="w-full max-w-[600px] m-auto p-1 rounded-md text-center">

          {/* <div className="flex justify-between" > */}
            <TabsList >
                {/* <TabsTrigger disabled={account_loading} className="text-sm!" value="transactions"><ArrowLeftRight />{wallettabs === "transactions" && "Transactions"}</TabsTrigger> */}
                <TabsTrigger disabled={account_loading} className="text-xs!" value="transactions"><ArrowLeftRight />Transactions</TabsTrigger>
                {/* <TabsTrigger disabled={account_loading} className="text-sm!" value="history"><History className="" />{wallettabs === "history" && "+History"}</TabsTrigger> */}
                <TabsTrigger disabled={account_loading} className="text-xs!" value="history"><History className="" />Top up History</TabsTrigger>
            </TabsList>
          {/* </div> */}
         {/* <Card className="px-0! py-[10px] m-0! w-full relative"> */}
            <TabsContents className="w-full relative">
               <TabsContent className="p-1" value="transactions">
                 <WalletTable {...{ }} />
               </TabsContent>
               <TabsContent value="history">
                  <WalletDeposits />
               </TabsContent>
            </TabsContents>
         {/* </Card> */}
      </Tabs>

    </>
  );
}


export default CoinWallet;


function WalletTable({ }){
  const simste = simpleStore()
  const [data, setData] = useState(undefined)
  // const [IsClient, setIsClient] = useState(false)
  const [loading, setLoading] = useState(false)
  const coinWalletTransactions = simste.pget(["coinWalletTransactions"])
  const currency = simste.pget(["cart"]).currency

   const theaddata = [
    {text:"Date", attrs:{className:"text-left text-xs! sm:text-sm! text-neutral-500!"}},
    {text:"Amount", attrs:{className:"text-right text-xs! sm:text-sm! text-neutral-500!"}},
    {text:"Purpose", attrs:{className:"text-right text-xs! sm:text-sm! text-neutral-500!"}},
    // {text:"Status", attrs:{className:"text-right pr-3!"}},
 ]


  useEffect(() => {
   const id = setTimeout(async () => {

        setLoading(true)
         const data = await fetchActionClient('GetCoinWalletTransaction', {})
         if(data?.detail === "Invalid token Error: HTTP 401") window.location.reload()
         setData(data)
        data && simste.pset(["coinWalletTransactions"], data) 
        setLoading(false)
        // setTimeout(()=>{setStartloading(false)},500)
      }, 0)

    return () => {
      clearTimeout(id)
    }
}, [currency])

useEffect(() => {
  simste.pset(["account_loading"], loading) 
}, [loading])

const dd = data || simste.pget(["coinWalletTransactions"])

  return (
    !(loading && !coinWalletTransactions) ?
    <Table>
        <TableHeader>
          <Thead headData={theaddata} />
        </TableHeader>
        <TableBody className="relative">
        {dd?.results?.length > 0 ?
          dd?.results.map((p, i)=>{
          return (
                <TRows key={`${p.id}${p.created_at}`} {...{p, i}} />
              )
          })
        :
        <TableRow>
          <TableCell
              colSpan={4}
              className="h-24 text-center"
          >
              No results.
          </TableCell>
        </TableRow>
        }
        </TableBody>
        <TableFooter className='w-full bg-transparent! border-none! hover:bg-transparent! shadow-none!' >
          <TableRow className='w-full bg-transparent! border-none! hover:bg-transparent! shadow-none!'>
              <TableCell colSpan={4} className='w-full  bg-transparent! border-none! hover:bg-transparent! shadow-none' >
                <div className='w-full flex flex-row justify-between gap-3 mt-3!' >
                  <div className="flex flex-row gap-3 w-1/2">

                  </div>
                  <div className="flex flex-row gap-3">
                    {dd?.page}
                  </div>
                  <div className="flex flex-row justify-end gap-3 w-1/2">
                    <Button disabled={!dd?.links?.previous} size='sm' variant='secondary' className='hover:ring-[0.5px] active:scale-95' >
                      Previous
                    </Button>
                    <Button disabled={!dd?.links?.next} size='sm' variant='secondary' className='hover:ring-[0.5px] active:scale-95' >
                      Next
                    </Button>
                  </div>
                </div>
              </TableCell>
          </TableRow>
        </TableFooter>
         {/* <Button onClick={(e)=>router.refresh()} >ffff</Button> */}
    </Table>
    :
     <div className="min-h-[200px]" >
        <Loading />
    </div>
  )
}