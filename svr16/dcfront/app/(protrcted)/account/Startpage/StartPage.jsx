"use client"
import React, { useRef, useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";
import { simpleStore, defStore } from '@/store/zustand_1'
import fetchActionClient from "@/app/actions/fetchActionBrowser";
import FormData from './Personal_data'

export default function StartPage() {

  const store = defStore()
  const simste = simpleStore()
  const userdata = simste.pget(["userdata"])
  // const [data, setData] = useState(undefined)
  const [IsClient, setIsClient] = useState(false)
  const [loading, setLoading] = useState(false)
  // const orders = tstore.pget(["orders"]) 

  
  useEffect(() => {
   const id = setTimeout(async () => {
        setLoading(true)
         const data = await fetchActionClient('GetUser', {})
         if(data?.detail === "Invalid token Error: HTTP 401") window.location.reload()
        data && simste.pset(["userdata"], data) 
        setLoading(false)
        // setTimeout(()=>{setStartloading(false)},500)
      }, 0)

    return () => {
      clearTimeout(id)
    }
  }, [])

  // console.log(userdata)
  useEffect(() => {
    simste.pset(["account_loading"], loading) 
  }, [loading])

  return (
    <div className="w-full">
      <FormData {...{ userdata, loading }} />
    </div>
  )
}
