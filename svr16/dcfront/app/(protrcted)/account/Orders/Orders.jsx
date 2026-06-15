"use client"
export const dynamic = "force-dynamic";
import React, { useRef, useEffect, useState } from "react";
import { createPortal } from "react-dom";
import { Badge } from "@/components/ui/badge"
import { Loader, SendHorizonal, Undo2, CircleX, HandCoins, CircleCheck, Disc3 } from "lucide-react"
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
import { Button } from "@/components/ui/button";
import { Thead, TRows } from './table/table.old'
import { useRouter } from "next/navigation";
import { tableStore } from '../tablestore'
import fetchActionClient from "@/app/actions/fetchActionBrowser";
import { simpleStore } from "@/store/zustand_1";
import Loading from '@/app/(protrcted)/account/loading'
import { TableWithSubtable } from "../Tables/TableWithSubtable";



function myQuerySelectAll(el, array=false){
  const els = typeof document !== 'undefined' ? document.querySelectorAll(el) : undefined
  return array ? Array.from(els) : els
}



const Orders = ({}) => {
  const tstore = tableStore()
  // const testref = useRef()
  const simste = simpleStore()
  const [data, setData] = useState(undefined)
  const [IsClient, setIsClient] = useState(false)
  const [loading, setLoading] = useState(false)
  const orders = simste.pget(["orders"]) 


  
  useEffect(() => {
   const id = setTimeout(async () => {
         setLoading(true)
         const Data = await fetchActionClient('GetOrder', {})
         if(Data?.detail === "Invalid token Error: HTTP 401") window.location.reload()
         setData(Data)
        Data && simste.pset(["orders"], Data) 
        !setLoading(false)
        // setTimeout(()=>{setStartloading(false)},500)
      }, 0)

    return () => {
      clearTimeout(id)
    }
  }, [])



  const theaddata = [
    {text:"Date", attrs:{className:"text-left text-xs! sm:text-sm! text-neutral-500!"}},
    {text:"Total", attrs:{className:"text-right text-xs! sm:text-sm! text-neutral-500!"}},
    {text:"Payment", attrs:{className:"text-left text-xs! sm:text-sm! text-neutral-500!"}},
    {text:"Status", attrs:{className:"text-right pr-3! text-xs! sm:text-sm! text-neutral-500!"}},
 ]

//############################################################
  const [a, setA] = useState(false)
  useEffect(()=>{
      // Table state wiederherstellen
      const tid = setTimeout(() => {
        const colaps = myQuerySelectAll('[data-colaps]')
        const clickrow = myQuerySelectAll('[data-clickrow]')
        if(!(colaps.length > 0 && tstore.tablestate)) setA((prev)=>!prev)
        if(colaps.length > 0 && tstore.tablestate){
          for (let i = 0; i < colaps.length; i++) {
            colaps[i].classList.value = tstore.tablestate.colapsClsVal[i]
            clickrow[i].classList.value = tstore.tablestate.clickrowClsVal[i]
          }
        }
      }, 100);
  
    return () => {
      clearTimeout(tid)
    }
  },[a])
//#############################################################

const statuses = {
      cancelled:<Badge variant="secondary" className="pointer-events-none bg-background border! border-secondary-foreground/50! dark:font-light py-1 pl-1" >
         <CircleX id="cancelled" className="w-full! min-w-[1rem]! h-full! min-h-[1rem] text-background fill-destructive" />
         Cancelled</Badge>,
      pending_payment:<Badge variant="secondary" className="pointer-events-none bg-background border! border-secondary-foreground/50! dark:font-light py-1 pl-1" >
         <HandCoins id="pending_payment" className="w-full! min-w-[1rem]! h-full! min-h-[1rem] animate-pulse text-orange-800 dark:text-orange-500" />
            Payment
         </Badge>,
      completed: <Badge variant="secondary" className="pointer-events-none bg-background border! border-secondary-foreground/50! dark:font-light py-1 pl-1" >
         <CircleCheck id="completed" className="fill-green-500 dark:fill-green-400 text-background min-w-[1rem] min-h-[1rem] rounded-full p-0! m-0!" />Completed</Badge>,

      refunded: <Badge variant="outlined" className="pointer-events-none bg-background border! border-secondary-foreground/50! dark:font-light py-1 pl-1" >
         <Undo2 id="refunded" className="w-full! min-w-[0.9rem]! h-full! min-h-[0.9rem]" />Refunded</Badge>,

      processing: <Badge variant="secondary" className="pointer-events-none bg-background border! border-secondary-foreground/50! dark:font-light py-1 pl-1" >
         <Loader id="processing" className="w-full! min-w-[0.9rem]! h-full! min-h-[0.9rem] text-blue-700 dark:text-blue-500" />
         Processing</Badge>,
   }

useEffect(()=>{
      orders && setData(orders)
      // orders && setData(tstore?.orders[`page_${orders.page}`])
  },[orders])

useEffect(() => {
  setIsClient(true)
}, [])

// function handleClick(e){
//       console.log(e.target.innerText)
// }

const dd = data || simste.pget(['orders'])

useEffect(() => {
  simste.pset(["account_loading"], loading) 
}, [loading])
  return (
    orders ?
    <div>
        <TableWithSubtable {...{ dd}} />
    </div>
    :
    <div className="min-h-[200px]" >
        <Loading />
    </div>
  );
}


export default Orders;
