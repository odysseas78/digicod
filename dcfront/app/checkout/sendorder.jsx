'use client'
import { cn } from '@/lib/utils'
import { useState, useEffect } from 'react'
import { useRouter, useParams, usePathname, useSearchParams } from "next/navigation";
import { Spinner } from '@/components/ui/spinner'
import fetchActionClient from '@/app/actions/fetchActionBrowser'

export default function SenOrder({store, simste, router, searchparams}) {
  const [open, setOpen] = useState(false)
  

  useEffect(()=>{
    const id = simste.pget(["cart"])?.total_products > 0 && 
    setTimeout(async () =>{
      const res = await fetchActionClient('OrderSend', {})
      if(res?.detail === "Invalid token Error: HTTP 401") window.location.reload()
      if(res.type === 'success') router.push(res.message)
    },300)

    return () => {
          clearTimeout(id)
        }
  },[])

  return (
    <div className={cn("fixed top-0 left-0 right-0 bottom-0 z-50 flex justify-center items-center backdrop-blur bg-background/10")}>
      <div className='z-50'>
         <Spinner className='size-18' />
         Processing...
      </div>
    </div>
  )
}
