"use client"
export const dynamic = "force-dynamic";
import React, { useRef, useEffect, useState } from "react";
import { useRouter, usePathname, useSearchParams, redirect } from "next/navigation"
import { Button } from "@/components/ui/button";
import TabsC from "@/app/(protrcted)/account/TabsC"
import { simpleStore } from "@/store/zustand_1";
import StartPage from '@/app/(protrcted)/account/Startpage/StartPage'
 import {
   Card,
   CardContent,
   CardDescription,
   CardFooter,
   CardHeader,
   CardTitle,
 } from '@/components/ui/card';
// import useDetectTouch from '@/hooks/useDetectTouch'

// function getCookie(name=null) {
//   if (typeof document === 'undefined') return null;
//   if(!name) return document.cookie;
//     return document.cookie.split('; ').find(row => row.startsWith(name + '='))?.split('=')[1]
// }


const Account = ({}) => {
  const routera = useRouter()
  const simste = simpleStore()



  

  return (
    <div className="w-full max-w-[800px] m-auto">
      {/* <Button onClick={(e)=>routera.refresh()} >ffff</Button> */}
      <TabsC {...{ }}  />
      {/* <Card className="px-[9px]! sm:px-[14px]!" >
         <StartPage />
      </Card> */}
     
      {/* <DataTableDemo /> */}
    </div>
  );
}


export default Account;
