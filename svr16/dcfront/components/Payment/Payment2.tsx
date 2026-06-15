"use client"
import {
   Field,
   FieldContent,
   FieldDescription,
   FieldGroup,
   FieldLabel,
   FieldSet,
   FieldTitle,
 } from "@/components/ui/field"
 import {
   RadioGroup,
   RadioGroupItem,
 } from "@/components/ui/radio-group"

import fetchActionClient from "@/app/actions/fetchActionBrowser"
import { defStore, simpleStore } from "@/store/zustand_1"
import { useEffect, useState } from "react"
import { getBasket } from "@/app/checkout/cart/cart"
import Loading from '@/components/Loader'
import { cn } from "@/lib/utils"
import { CheckCheckIcon, CheckCircle, TrendingUpIcon } from "lucide-react"
import ReactDOM from 'react-dom';
import wk from '@/lib/wk'
 
const refo = wk.refs
const $s = wk.signalP

 export default function Payment() {
   const store = defStore()
   const simste = simpleStore()
   const cart = simste.pget(["cart"])
   const currency = cart?.currency
   const selpayment = cart?.payment_method
  //  const [response, setResponse]  = useState()
   const [loading, setLoading]  = useState(false)
   // useEffect(()=>{setSelPayment2(selpayment?.id)},[selpayment])
   


   
   useEffect(() => {
     const id = setTimeout(async () => {
        setLoading(true)
       const res = await fetchActionClient('GetPayment', {})
       if(res?.detail === "Invalid token Error: HTTP 401") window.location.reload()
       simste.pset(["GetPayment"], res)
      //  setResponse(res)
       setLoading(false)
     }, 30)
     return () => {
       clearTimeout(id)
     }
   }, [])

   const payments = simste.pget(["GetPayment"])

   async function onValueChangeHandle(e:string){
      // console.log(e);
      
      const res = await getBasket(simste,{ addpayment: e })
      
   }


   return (
    <>
    {(simste.pget(["basketloader"]) || loading) && <Loading />}
    
     <div className="flex flex-row flex-wrap w-full! justify-center items-center m-0 p-0 min-h-100">
      
       <FieldGroup className="flex flex-row justify-center items-center w-full! p-0! m-0!">
         <FieldSet className="flex flex-col justify-center items-center w-full! p-0! m-0!">
           {/* <FieldLabel htmlFor="compute-environment">
             Select Payment Method
           </FieldLabel> */}
               
           <RadioGroup 
               defaultValue={cart.payment_method?.id} 
               value={cart.payment_method?.id} 
               onValueChange={onValueChangeHandle} 
               className="flex flex-row flex-wrap justify-center w-full! gap-3 max-w-max! items-center p-0! m-0! pt-[10px]!">
            {
               payments && payments.length > 0 && payments.map((p:any)=>{
                  return (
                     <FieldLabel key={p.id} htmlFor={`${p.id}${p.name}`} 
                        className={cn("flex flex-col justify-center items-center shadow m-0! p-0! shadow-neutral-300! dark:shadow-neutral-600! max-w-max w-min relative",
                           (`${cart.payment_method?.id}` === `${p.id}` ? "ring-1! ring-green-600! dark:ring-green-500! border! border-green-500! dark:border-green-500!":"")
                        )}>
                           
                          {cart.payment_method?.id === p.id && <CheckCircle className="absolute top-[-8px] right-[-8px] bg-secondary! w-[1.15rem] h-[1.15rem] rounded-full text-green-600 dark:text-green-500" />}

                        <Field orientation="vertical" className="flex flex-col justify-between items-center w-max p-[2px]! m-0!">
                           <FieldContent className="flex flex-col justify-between items-center gap-[5px] p-0! m-0!">
                              {p.name === "Wallet" ? <img src={p.image} className='rounded-md w-[90px] h-[90px] p-0 m-0' />
                              :
                              <>
                              <img src={p.image} className='rounded-md w-[90px] h-[43px] p-0 m-0' />
                              <div className='text-sm p-0 flex flex-col justify-center items-center w-full'>
                                 {(p?.fee_rate > 0) ? <small>fee {p?.fee_rate}%</small>:<small>free</small> }
                                 {(p?.fee_fix > 0) ? <small>+ {p?.fee_fix} {currency?.sign}</small>:<small className="text-transparent" >free</small>}
                              </div>
                              </>}
                           </FieldContent>
                           <RadioGroupItem value={p.id} id={`${p.id}${p.name}`} className="scale-0 hidden" />
                        </Field>
                     </FieldLabel>
                  )
               })
            }
           </RadioGroup>
         </FieldSet>
       </FieldGroup>
     </div>
     </>
   )
 }
 
