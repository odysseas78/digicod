"use client"
export const dynamic = "force-dynamic";
import React, { useRef, useEffect, useState } from "react";
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
import { Button } from "@/components/ui/button";
import { Thead, TRows } from './table/table'
import { useRouter } from "next/navigation";
import { tableStore } from '../../tablestore'
import fetchActionClient from "@/app/actions/fetchActionBrowser";
import { simpleStore } from "@/store/zustand_1";
import Loading from '@/app/(protrcted)/account/loading'



function myQuerySelectAll(el, array=false){
  const els = typeof document !== 'undefined' ? document.querySelectorAll(el) : undefined
  return array ? Array.from(els) : els
}



const WalletDeposits = ({}) => {
  const tstore = tableStore()
  const testref = useRef()
  const simste = simpleStore()
  const [data, setData] = useState(undefined)
  const [IsClient, setIsClient] = useState(false)
  const [loading, setLoading] = useState(false)
  const wdeposits = simste.pget(["wdeposits"]) 


  
  useEffect(() => {
   const id = setTimeout(async () => {
        setLoading(true)
         const Data = await fetchActionClient('GetCoinWalletDeposit', {})
         if(Data?.detail === "Invalid token Error: HTTP 401") window.location.reload()
         setData(Data)
        Data && simste.pset(["wdeposits"], Data) 
        setLoading(false)
        // setTimeout(()=>{setStartloading(false)},500)
      }, 0)

    return () => {
      clearTimeout(id)
    }
  }, [])



  const theaddata = [
    {text:"Date", attrs:{className:"text-left text-xs! sm:text-sm! text-neutral-500!"}},
    {text:"Total", attrs:{className:"text-right text-xs! sm:text-sm! text-neutral-500!"}},
    {text:"Payment", attrs:{className:"text-right text-xs! sm:text-sm! text-neutral-500!"}},
    {text:"Status", attrs:{className:"text-right pr-3! text-xs! sm:text-sm! text-neutral-500!"}},
 ]

//############################################################
  const [a, setA] = useState(false)
  useEffect(()=>{
      // Table state wiederherstellen
      const tid = setTimeout(() => {
        const colaps = myQuerySelectAll('[data-colaps]')
        const clickrow = myQuerySelectAll('[data-clickrow]')
        if(!(colaps.length > 0 && tstore.wdtablestate)) setA((prev)=>!prev)
        if(colaps.length > 0 && tstore.wdtablestate){
          for (let i = 0; i < colaps.length; i++) {
            colaps[i].classList.value = tstore.wdtablestate.colapsClsVal[i]
            clickrow[i].classList.value = tstore.wdtablestate.clickrowClsVal[i]
          }
        }
      }, 100);
  
    return () => {
      clearTimeout(tid)
    }
  },[a])
//#############################################################



useEffect(()=>{
      wdeposits && setData(wdeposits)
      // orders && setData(tstore?.orders[`page_${orders.page}`])
  },[wdeposits])

useEffect(() => {
  setIsClient(true)
}, [])

useEffect(() => {
  simste.pset(["account_loading"], loading) 
}, [loading])

const dd = data || simste.pget(['wdeposits'])
const loading2 = loading && !wdeposits
  return (
    !loading2 ?
    <Table>
        <TableHeader>
          <Thead headData={theaddata} />
        </TableHeader>
        <TableBody className="relative">
        {dd?.results?.length > 0 ?
          dd?.results.map((p)=>{
          return (
                <TRows key={`${p.id}${p.created_at}`} {...{p, testref}} />
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
  );
}


export default WalletDeposits;
