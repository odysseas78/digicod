"use client"
export const dynamic = "force-dynamic";
import wk from "@/lib/wk";
import { cn } from '@/lib/utils'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { simpleStore, defStore } from '@/store/zustand_1'
import { postBasket } from "@/app/checkout/cart/cart";
import React, { useCallback, useEffect, cache, useState, useDeferredValue, useRef } from "react";
// import { signal } from "@preact/signals-react";
import fetchClient from "@/app/actions/fetchClient";


function setCookie(name, value, days = 365) {
    const expires = new Date(Date.now() + days * 864e5).toUTCString();
    document.cookie = `${name}=${value}; expires=${expires}; path=/; SameSite=Lax`;
}

export default function CurrSel({ fcurrency, fbasket }) {
  "use client"
  const store = defStore()
  const simste = simpleStore()
  const cart = simste.pget(["cart"])
  // const cart = simste.pget(["cart"]) || fbasket?.cart
  const storcurrencyes = store.dget(["currencyes"]) || fcurrency
  const storcurrency = store.dget(["currency"])
  const [curdat, setCurdat] = useState(storcurrencyes || fcurrency || [])

  const [IsClient, setIsClient] = useState(false)
    useEffect(() => {
     setIsClient(true)
  }, [])
  
  const unauth = (fbasket?.unauthorized || fcurrency?.unauthorized)
  if(unauth === 401){
    console.log(unauth)
  }
  
  useEffect(() => {
      !storcurrency && store.dset(['currency'], cart?.currency)
      const id = setTimeout(async () => {
      const response = await fetchClient("GET", "currency")

      if(response?.detail === "Invalid token Error: HTTP 401") window.location.reload()
      // console.log('response', response)
      setCurdat(response)
      store.dset(['currencyes'], response)
    }, 0)
    return () => {
      clearTimeout(id)
    }
  },[])
  
  const storcur = storcurrencyes && storcurrencyes?.filter((f) => f?.id === cart?.currency?.id)?.[0]
  const datacur = fcurrency && fcurrency[0]?.id && fcurrency?.filter((f) => f?.id === fbasket?.cart?.currency?.id)?.[0]
  const [selected, setSelected] = useState(storcur || datacur)
  const isFirstRender = useRef(true)
  

  useEffect(() => {
    if(storcurrency?.id !== cart?.currency?.id){
      store.dset(['currency'], cart?.currency)
    }
    
    // setCookie("_hkl", storcurrency?.id)
  }, [cart?.currency])

  


  useEffect(()=>{

    (selected?.id || cart?.currency?.id) && wk.encryptWithPublicKey( JSON.stringify({cur_id:(selected.id || cart?.currency?.id)}), wk.cryptkey).then((r)=>setCookie("_hkl", r))
    if (isFirstRender.current) {
      isFirstRender.current = false
      return
    }
   
  },[selected])

  const handleChange = (e) => {
    const nextSelected = curdat?.find((f) => f.shortname === e)
    if (!nextSelected) return
    console.log(selected)
    setSelected(nextSelected)
    postBasket(simste, { action:"currency", currency_id: nextSelected.id })
    store.dset(["currency"], nextSelected)
  }

  const selectedShortname = IsClient
    ? (store.dget(["currency"])?.shortname || storcurrency?.shortname)
    : undefined



// if(!IsClient) return
  // const blurbackdrop = <div className={cn('top-0 left-0 z-50 right-0 bottom-0 absolute flex items-center justify-center backdrop-blur rounded-md bg-background/80 animate-pulse')} ></div>
  return (
    <div suppressHydrationWarning>
    <Select 
        onValueChange={handleChange} 
        value={selectedShortname }
        translate="no" >
          
      <SelectTrigger translate="no" className="w-full! min-w-max! max-w-max! m-0! py-[3px]! px-[8px]! flex justify-center text-[0.75rem]! sm:text-[0.85rem]! items-center rounded-sm cursor-pointer h-full! min-h-min! max-h-max!  relative">
      <SelectValue placeholder={`${datacur?.shortname} ${datacur?.sign}` || `USD $`} />
      {/* <SelectValue placeholder={`${(selected?.shortname || storcurrency?.shortname)} ${(selected?.sign || storcurrency?.sign)}`} /> */}
       {/* {!(store.currency?.shortname) && blurbackdrop}
       {!(store.currency?.shortname) ? <div>Currency</div>: <SelectValue placeholder='' />} */}
      </SelectTrigger>
      <SelectContent translate="no" position='popper' className="text-[0.75rem]! sm:text-[0.85rem]! w-full! min-w-[50px]! max-w-max!">
        {
          (curdat || datacur)?.map((m) => (
            <SelectItem translate="no" className="w-full max-w-[90px]! text-[0.75rem]! sm:text-[0.85rem]!" key={m.shortname} value={m.shortname}>{m.shortname || `USD`} {m.sign || `$`}</SelectItem>
          ))
        }
      </SelectContent>
    </Select>
     
    </div>
  )

}
