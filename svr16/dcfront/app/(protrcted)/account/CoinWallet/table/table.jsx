"use client"
export const dynamic = "force-dynamic";
import React, { useRef, useEffect, useState } from "react";
import Link from 'next/link';
import { Loader, BanknoteArrowDown, Undo2, CircleX, HandCoins, CircleCheck, Disc3 } from "lucide-react"
import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
  } from "@/components/ui/table"
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge"
import { nanoid } from 'nanoid';
import { create } from 'zustand';
import { persist, devtools } from 'zustand/middleware'
import { simpleStore } from "@/store/zustand_1";
import {
   Field,
   FieldDescription,
   FieldGroup,
   FieldLabel,
   FieldLegend,
   FieldSeparator,
   FieldSet,
 } from "@/components/ui/field"
 import { Input } from "@/components/ui/input"
 import { tableStore } from '../../tablestore'
 import { cn } from '@/lib/utils'

 function currencyFormat(amount, currency){
   const formatted = new Intl.NumberFormat("de-DE", {
     style: "currency",
     currency: currency,
   }).format(amount)
   return formatted
 }

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


export function Thead({headData, rowsData}) {
   // headData = [{text:"Date", attrs:{className:"w-full"}}] Array
   // rowsData = {attrs:{className:"h-6"}} object

  
  const contentels = headData.map((c)=>{
   return (
      <TableHead key={c.text} {...c.attrs} >{c.text}</TableHead>
   )
  })

  return (
         <TableRow {...rowsData?.attrs} >
            {contentels}
         </TableRow>
  )
}





 function toggleClaslist(elclslist,clsList){
   for (const cls of  clsList){
      elclslist.toggle(cls)
   }
}

function myQuerySelectAll(el, array=false){
   const els = typeof document !== 'undefined' ? document.querySelectorAll(el) : undefined
   return array ? Array.from(els) : els
}

function classlistArray(el){
   return typeof document !== 'undefined' ? Array.from(el.classList) : undefined
}

function tableStateSave(tstore){
   const colapsArr = myQuerySelectAll('[data-colaps]', true)
   const colapsClsVal = colapsArr.map((c)=>c.classList.value)
   const clickrowArr = myQuerySelectAll('[data-clickrow]', true)
   const clickrowClsVal = clickrowArr.map((c)=>c.classList.value)
   tstore.pset(["wtablestate"], {colapsClsVal:colapsClsVal, clickrowClsVal:clickrowClsVal})
}

export function TRows({p, testref, i}){
   const tstore = tableStore()
   const collapsref = useRef()
   const simste = simpleStore()
   const coinWalletTransactions = simste.pget(["coinWalletTransactions"]) 
   // const statuses = {
   //    cancelled:<Badge variant="secondary" className="pointer-events-none bg-background border! border-secondary-foreground/50! dark:font-light py-1 pl-1" >
   //       <CircleX className="w-full! min-w-[1rem]! h-full! min-h-[1rem] text-background fill-destructive" />
   //       Cancelled</Badge>,
   //    pending_payment:<Badge variant="secondary" className="pointer-events-none bg-background border! border-secondary-foreground/50! dark:font-light py-1 pl-1" >
   //       <HandCoins className="w-full! min-w-[1rem]! h-full! min-h-[1rem] animate-pulse text-orange-800 dark:text-orange-500" />
   //          Payment
   //       </Badge>,
   //    completed: <Badge variant="secondary" className="pointer-events-none bg-background border! border-secondary-foreground/50! dark:font-light py-1 pl-1" >
   //       <CircleCheck className="fill-green-500 dark:fill-green-400 text-background min-w-[1rem] min-h-[1rem] rounded-full p-0! m-0!" />Completed</Badge>,

   //    refunded: <Badge variant="outlined" className="pointer-events-none bg-background border! border-secondary-foreground/50! dark:font-light py-1 pl-1" >
   //       <Undo2 className="w-full! min-w-[0.9rem]! h-full! min-h-[0.9rem]" />Refunded</Badge>,

   //    processing: <Badge variant="secondary" className="pointer-events-none bg-background border! border-secondary-foreground/50! dark:font-light py-1 pl-1" >
   //       <Loader className="w-full! min-w-[0.9rem]! h-full! min-h-[0.9rem] text-blue-700 dark:text-blue-500" />
   //       Processing</Badge>,
   // }

   
   
   // console.log(myQuerySelectAll('[data-colaps]'))
   // tstore.tablestate && console.log(tstore.tablestate)
   // if(tstore.tablestate?.clslist && tstore.tablestate?.el){
   //    tstore.tablestate.clslist = tstore.tablestate.clslist
   //    tstore.tablestate.el = tstore.tablestate.el
   // }
   const handleRowClick = (e) => {
      // const clslist = collapsref.current?.classList
      // const colaps = myQuerySelectAll('[data-colaps]')
      // const clickrow = myQuerySelectAll('[data-clickrow]')

      
  
      // console.log(myQuerySelectAll('[data-colaps]'))
      if(clslist){
         if(clslist.contains('grid-rows-[1fr]!')){
            toggleClaslist(clslist, ['grid-rows-[0fr]!', 'grid-rows-[1fr]!'])
            toggleClaslist(e.target.parentElement.classList, ['shadow-inner!', 'shadow-neutral-400/70!', 'dark:shadow-neutral-500/70!'])
         } else {
            toggleClaslist(clslist, ['grid-rows-[1fr]!', 'grid-rows-[0fr]!'])
            toggleClaslist(e.target.parentElement.classList, ['shadow-inner!', 'shadow-neutral-400/70!', 'dark:shadow-neutral-500/70!'])
         }
         for (const l of colaps){
            if(clslist !== l.classList && l.classList.contains('grid-rows-[1fr]!')){
               toggleClaslist(l.classList, ['grid-rows-[1fr]!', 'grid-rows-[0fr]!'])
            }
         }
         for (const l of clickrow){
            if(e.target.parentElement.classList !== l.classList && l.classList.contains('shadow-neutral-400/70!')){
               toggleClaslist(l.classList, ['shadow-inner!', 'shadow-neutral-400/70!', 'dark:shadow-neutral-500/70!'])
            }
         }
         tableStateSave(tstore)
      }
   }
 
   
   
   const theaddata = [
      {text:"Product", attrs:{className:"text-left h-8!"}},
      {text:"Qty", attrs:{className:"text-right h-8!"}},
      {text:"Price", attrs:{className:"text-right h-8!"}},
      {text:"Total", attrs:{className:"text-right h-8!"}},
   ]

   return (
      <>
      <TableRow 
         data-clickrow='a' 
         // onPointerUp={handleRowClick} 
         className={cn("text-left text-xs! sm:text-sm!", (coinWalletTransactions.total-1 === i ? "border-b!" : ""))}>
         <TableCell > 
            {dateFormat(p.created_at, "dateonly")}
         </TableCell>
         <TableCell className={cn("text-right")}> 
            <span className="pointer-events-none">{p.dcamount} DC</span>&ensp;
            <span className="text-right italic pointer-events-none">
               (≈ {currencyFormat(p.amount, simste.pget(["cart"]).currency.shortname)})
            </span>
             
         </TableCell>
         <TableCell className="text-right"> 
            {p.purpose}
         </TableCell>
      </TableRow >
      {/* ############ SUBTABLE ####### */}
      {/* <TableRow className="p-0! m-0! border-0">
         <TableCell colSpan={4} className="p-0! m-0! max-w-full" >
            <div data-colaps='a' ref={collapsref} className="grid! grid-cols-1 grid-rows-[0fr]! overflow-hidden! m-0! p-0! transition-all duration-300">
               <div ref={testref} data-ref={p.id} className='min-h-0' >
                  <div className="m-[2px] p-[1px] max-w-full bg-background rounded-b-sm! shadow shadow-neutral-400/70 dark:shadow-neutral-500/70">
                     <div className='w-full flex flex-row justify-start gap-3 p-3 border-b' >
                       lkjlkjlj
                     </div>
                  </div>
               </div>
            </div>
         </TableCell>
      </TableRow > */}
       {/* ############################# */}
      </>
   )
}





function Collapse({children, trigger, p}){
   const [open, setOpen] = useState()
   const collapsref = useRef()
   const rstore = rowsStore()
   const simste = simpleStore()

   useEffect(()=>{
      console.log(trigger)
      const clsList = collapsref.current?.classList
      // console.log(trigger)
      rstore.set((prev)=>{
         // console.log(prev)
         const h = {...prev}
         h.collap[p.id] = clsList

         return {...h}})
      
      if(clsList.contains('grid-rows-[1fr]!')){
         clsList.toggle('grid-rows-[0fr]!')
         clsList.toggle('grid-rows-[1fr]!')   
         setOpen(false)   
      } else {
         clsList.toggle('grid-rows-[1fr]!')
         clsList.toggle('grid-rows-[0fr]!')
         setOpen(true)
      }
      const gg = rstore.collap
         gg && console.log(gg)
         for (const l of Object.keys(gg)){

            if(Number(l) !== Number(trigger[0]) && gg[l].contains('grid-rows-[1fr]!')){
               gg[l].toggle('grid-rows-[0fr]!')
               gg[l].toggle('grid-rows-[1fr]!')
            }
         }
   },[trigger[1]])
   


   return (
      <div ref={collapsref} className="grid! grid-cols-1 grid-rows-[0fr]! overflow-hidden! m-0! p-0! transition-all duration-300 max-w-full">
         <div className='min-h-0'>
            {children}
         </div>
      </div>
   )
}