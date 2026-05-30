"use client"
import { simpleStore } from '@/store/zustand_1'
import {testAction} from '@/app/actions/test';
import { useParams, useRouter, usePathname, useSearchParams } from "next/navigation";






export default function TestButton({ unauth }){
      const simste = simpleStore()
      const router = useRouter()
   // console.log(unauth)
   // if(unauth === 401) testAction(unauth)


   return (
      // <button className="border border-green-500 rounded-full" onClick={(e)=>simste.pset(['GustaW'], {hhhh:12345, hhh:9999})} >
      <button className="border border-green-500 rounded-full" onClick={(e)=>console.log(simste)} >
      {/* <button className="border border-green-500 rounded-full" onClick={(e)=>router.push('/')} > */}
         BB
      </button>
   )
}