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
import { Trash2 } from 'lucide-react';
 import { Input } from "@/components/ui/input"
 import { tableStore } from '../../../tablestore'
 import { SimplDialog } from '@/components/Dialogs/MainDialog'



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
   tstore.pset(["wdtablestate"], {colapsClsVal:colapsClsVal, clickrowClsVal:clickrowClsVal})
}

export function TRows({p, testref}){
   const tstore = tableStore()
   const collapsref2 = useRef()
   const simste = simpleStore()
   const cart = simste.pget(['cart'])
   const statuses = {
      cancelled:<Badge variant="secondary" className="pointer-events-none bg-background border! border-secondary-foreground/50! dark:font-light py-1 pl-1" >
         <CircleX className="w-full! min-w-[1rem]! h-full! min-h-[1rem] text-background fill-destructive" />
         Cancelled</Badge>,
      pending_payment:<Badge variant="secondary" className="pointer-events-none bg-background border! border-secondary-foreground/50! dark:font-light py-1 pl-1" >
         <HandCoins className="w-full! min-w-[1rem]! h-full! min-h-[1rem] animate-pulse text-orange-800 dark:text-orange-500" />
            Payment
         </Badge>,
      completed: <Badge variant="secondary" className="pointer-events-none bg-background border! border-secondary-foreground/50! dark:font-light py-1 pl-1" >
         <CircleCheck className="fill-green-500 dark:fill-green-400 text-background min-w-[1rem] min-h-[1rem] rounded-full p-0! m-0!" />Completed</Badge>,

      refunded: <Badge variant="outlined" className="pointer-events-none bg-background border! border-secondary-foreground/50! dark:font-light py-1 pl-1" >
         <Undo2 className="w-full! min-w-[0.9rem]! h-full! min-h-[0.9rem]" />Refunded</Badge>,

      processing: <Badge variant="secondary" className="pointer-events-none bg-background border! border-secondary-foreground/50! dark:font-light py-1 pl-1" >
         <Loader className="w-full! min-w-[0.9rem]! h-full! min-h-[0.9rem] text-blue-700 dark:text-blue-500" />
         Processing</Badge>,
   }

   
   
   // console.log(myQuerySelectAll('[data-colaps]'))
   // tstore.tablestate && console.log(tstore.tablestate)
   // if(tstore.tablestate?.clslist && tstore.tablestate?.el){
   //    tstore.tablestate.clslist = tstore.tablestate.clslist
   //    tstore.tablestate.el = tstore.tablestate.el
   // }
   const handleRowClick = (e) => {
      const clslist = collapsref2.current?.classList
      const colaps = myQuerySelectAll('[data-colaps]')
      const clickrow = myQuerySelectAll('[data-clickrow]')

      
  
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
 
   

   useEffect(()=>{
      if(testref.current){
         // if(Number(testref.current.getAttribute('data-ref')) === p.id) console.log(testref.current.getAttribute('data-ref'),  p.id)
      }
   },[])
   
   const theaddata = [
      {text:"Product", attrs:{className:"text-left h-8! text-neutral-400! italic! font-bold text-sm!"}},
      {text:"Qty", attrs:{className:"text-right h-8! text-neutral-400! italic! font-bold text-sm!"}},
      {text:"Price", attrs:{className:"text-right h-8! text-neutral-400! italic! font-bold text-sm!"}},
      {text:"Total", attrs:{className:"text-right h-8! text-neutral-400! italic! font-bold text-sm!"}},
   ]

   const content = 
   <div className="flex flex-col justify-center items-center gap-[20px]" >
      <div>Do you want to delete the entry?</div>
      <div className="flex flex-row justify-end items-center w-full gap-[15px]" >
         <Button size="sm" variant="default" className="active:scale-90" >Close</Button>
         <Button 
            variant="outline"
            className="active:scale-90 text-red-500"
            size="sm"
            onPointerUp={(e)=>{
            if(e.button === 0){
               // setSendorder(true)
               // store.Set({sendorder:true})
               // router.push('/checkout?c=payment')
            }
            }}
            >
               <Trash2 className='w-full m-0 pointer-events-none' width={300} />
            Delete
         </Button>
      </div>
      
      
   </div>

   const onClickDelete =()=>{
      const id = nanoid()
      simste.pset(["simpldialogs", `${id}`], 
   <SimplDialog {...{title: 'Warning', content: content, type: 'warning', trigger: 1, fn: null, id}} />)
   }

   return (
      <>
      <TableRow data-clickrow='a' onPointerUp={handleRowClick} className="text-left">
         <TableCell className="text-right text-xs! sm:text-sm!" > 
            {dateFormat(p.created_at, "dateonly")}
         </TableCell>
         <TableCell className="text-right text-xs! sm:text-sm!"> 
            {p.total.b} {cart.currency.sign}
         </TableCell>
         <TableCell className="text-right text-xs! sm:text-sm!"> 
            {cart.payment_method.name}
         </TableCell>
         <TableCell className="text-right text-xs! sm:text-sm!">
             {statuses[p.status]}
         </TableCell>
      </TableRow >
      {/* ############ SUBTABLE ####### */}
      <TableRow className="p-0! m-0! border-0">
         <TableCell colSpan={4} className="p-0! m-0! max-w-full" >
            <div data-colaps='a' ref={collapsref2} className="grid! grid-cols-1 grid-rows-[0fr]! overflow-hidden! m-0! p-0! transition-all duration-300">
               <div className='min-h-0' >
               {/* <Collapse trigger={collapse} p={p} > */}
                  <div className="m-[2px] p-[1px] max-w-full bg-background rounded-b-sm! shadow shadow-neutral-400/70 dark:shadow-neutral-500/70">
                     <div className='w-full flex flex-row flex-wrap justify-start gap-3 p-3 border-b' >
                        <div className="w-full text-left" >
                           <span className="text-xs mr-[6px] italic! text-neutral-400! font-bold" >ID:</span>
                           <span className="text-xs">{p.uuid}</span>
                        </div>
                        {p.status === 'completed' && <Button size='xs' variant='secondary' className='hover:ring-[0.5px] active:scale-95 rounded-sm' >
                           Resend purchase email
                        </Button>}
                        {
                        //    <Button 
                        //    onClick={(e)=>onClickDelete(e)}
                        //    disabled={p.status === 'processing'} size='xs' variant='secondary' className='hover:ring-[0.5px] active:scale-95 rounded-sm' >
                        //    Delete
                        // </Button>
                           <Alertdialog 
                              {...{ 
                                    title:"Delete?", 
                                    description: "Do you want to delete the entry?",
                                    action: "Delete"
                                    }} >
                              <Button 
                              // size="xs" variant="destructive">
                                 disabled={p.status === 'processing'} size='xs' variant='destructive' className='hover:ring-[0.5px] active:scale-95 rounded-sm'>
                                     <Trash2Icon className="max-w-5! max-h-5!" size="sm" />
                                 Delete
                              </Button>
                           </Alertdialog>
                        }
                        {(p.status === 'pending_payment' && p.responsedata.message) && <Link 
                           size='xs'
                           href={`${p.responsedata.message}`}
                           // target="_blank"
                           variant='secondary' 
                           className='hover:ring-[0.5px] active:scale-95 rounded-sm bg-accent text-xs py-[3px] px-[5px] max-h-min' >
                           Pay Now
                        </Link>}
                        {/* <Field >
                           <Input size='xs' className="w-30! h-6!" />
                        </Field> */}
                     </div>
                  </div>
                  {/* </Collapse> */}
               </div>
            </div>
         </TableCell>
      </TableRow >
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


import { Trash2Icon } from "lucide-react"

import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogMedia,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog"


export function Alertdialog({children, title, description, action}) {
  return (
    <AlertDialog size="sm" >
      <AlertDialogTrigger size="sm" asChild>
        {children}
      </AlertDialogTrigger>
      <AlertDialogContent size="sm">
        <AlertDialogHeader size="sm" >
          <AlertDialogMedia size="sm" className="bg-destructive/10 text-destructive dark:bg-destructive/20 dark:text-destructive flex w-10 h-10">
            <Trash2Icon className="max-w-5! max-h-5!" size="sm" />
          </AlertDialogMedia>
          <AlertDialogTitle size="sm" >{title}</AlertDialogTitle>
          <AlertDialogDescription size="sm" >
            {description}
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter size="sm" className="-mx-6 -mb-6 flex flex-col-reverse gap-2 rounded-b-xl border-t bg-muted/50 p-4 group-data-[size=sm]/alert-dialog-content:grid group-data-[size=sm]/alert-dialog-content:grid-cols-2 sm:flex-row sm:justify-end" >
          <AlertDialogCancel className='hover:ring-[0.5px]! active:scale-95! rounded-sm!' size="sm" variant="outline">Cancel</AlertDialogCancel>
          <AlertDialogAction className='hover:ring-[0.5px]! active:scale-95! rounded-sm!' size="sm" variant="destructive">{action}</AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  )
}