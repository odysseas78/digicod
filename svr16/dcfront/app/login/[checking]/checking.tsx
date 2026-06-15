'use client';
import React, { useEffect } from "react";
import fetchActionClient from "@/app/actions/fetchActionBrowser";
import Loading from "@/components/Loader"
import { useRouter, usePathname, useSearchParams, redirect } from "next/navigation"
import { simpleStore, defStore } from "@/store/zustand_1"
import { SimplDialog } from '@/components/Dialogs/MainDialog'
import { nanoid } from 'nanoid'
import { SetCookies } from '@/app/actions/setcookies'





export default function LoginChecking ({token}:any) {
   const simste = simpleStore()
   const router = useRouter()
   const pathname = usePathname()
   const searchparams = useSearchParams()

   // console.log('checking', token);
   

   useEffect(() => {
       
      let tid:any
      if(pathname === '/login/chcke') {
         tid = setTimeout(() => {
            // simste.setdialog({ title:'Error', message:'The link is invalid or has expired.', status:'error', trigger:1, fn: ()=>router.replace('/login')})
            // ###########  Dialog Messages #############################
               // const tid = setTimeout(() => {
                  const id = nanoid()
                     // const capitalized = response.type.charAt(0).toUpperCase() + response.type.slice(1)
                     simste.pset(["simpldialogs", `${id}`], 
                  <SimplDialog {...{title: 'Error', content: 'The link is invalid or has expired.', type: 'error', trigger: 1, fn: ()=>router.replace('/login'), id}} />)
               // }, 0)
            // ############# end Dialog Messages ###################3####
            // console.log(pathname)
            }, 100);
            } 

      return () => {
         clearTimeout(tid)
      }

   }, []);

  
   useEffect(() => {
       
      const tid:any = token.length > 20 && setTimeout(async () => {
         const res = await fetchActionClient('LoginRegister', { filter: { urltoken:token } })
         if(res?.detail === "Invalid token Error: HTTP 401") window.location.reload()
         if(res.type === 'success' && res.auth_token) {
            // await SetCookies("set", "auth_token", `${res.auth_token}`)
            await simste.pget(["getBasket"])(simste, {})
            router.replace('/account')
            // window.location.href = '/account';
         } else if(res.type === 'error') {
            // router.push('/login?error=invalid-link')
            router.replace('/login/chcke')
            
            // window.location.href = '/login?error=invalid-link';
         }
         
      }, 0);

      (token.length < 20 && pathname !== '/login/chcke') && router.replace('/login/chcke')

      return () => {
         clearTimeout(tid)
      }

   }, []);
   

   return (
      <Loading  />
   )

}
