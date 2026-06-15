//@ts-nocheck
"use client"
// export const dynamic = "force-dynamic";
import {
  Popover,
  PopoverAnchor,
  PopoverContent,
  PopoverTrigger
} from "@/components/ui/popover";
import wk from "@/lib/wk";
import * as React from 'react';
import { useEffect, useRef, useState } from "react";
import Payments from "./Payment";
import { defStore, simpleStore } from '@/store/zustand_1';


const refo = wk.refo
const $s = wk.signalP
$s.paypopover = false
$s.setOpen = null
export default function PaymentPopover({

  children, el, anhor
}: {
  children: React.ReactNode
}) {
  const elref = useRef(null)

  const store = defStore()
  const simstore = simpleStore()
  // st.rrr = 123
  // 
  const [open, setOpen] = useState(false)


  $s.setOpen.value = setOpen

  // 
  useEffect(() => {
    const tm = setTimeout(() => {

      clearTimeout(tm)
    }, 500)
    $s.paypopover.value = open
    // 

  }, [open])



  return (
    <>


      <Popover open={open} container={anhor} onOpenChange={(e) => {
        setOpen(e)

      }} >

        <div className="">
          <PopoverTrigger ref={elref} asChild>
            {children}
          </PopoverTrigger>
        </div>

        <div className='w-[30%] left-1/2 bottom-0 -translate-x-1/2 opacity-0 absolute m-auto min-w-max bg-transparent' >
          <PopoverAnchor >
          </PopoverAnchor>
        </div>
        <PopoverContent className="w-full min-w-[360px] max-w-[100vw] mx-auto flex-row flex-wrap container">
          <Payments />
        </PopoverContent>
      </Popover>
    </>
  )

}

