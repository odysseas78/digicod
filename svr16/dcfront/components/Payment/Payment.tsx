//@ts-nocheck
"use client"
// export const dynamic = "force-dynamic";

// import useAxiosFunction from '@/hooks/useAxiosFunction';
import { cn } from '@/lib/utils';
import wk from '@/lib/wk';
import {
  CircleCheckBig
} from 'lucide-react';
import { use, useEffect, useState } from 'react';
import Loading from '@/components/Loader'

import { TrendingDownIcon, TrendingUpIcon } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import {
  Card,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import {
  RadioGroup,
  RadioGroupItem,
} from "@/components/ui/radio-group"
import fetchActionClient from "@/app/actions/fetchActionBrowser";
import { getBasket } from "@/app/checkout/cart/cart";
import { defStore, simpleStore } from '@/store/zustand_1';


  // ############################################
  function mergeUniqueKeys<T extends Record<string, any>>(target: T, source: Record<string, any>): T {
    const seenKeys = new Set<string>();
  
    function recursiveMerge(target: any, source: any) {
      if (typeof source !== "object" || source === null) {
        return;
      }
      for (const key in source) {
        if (key in target && !seenKeys.has(key)) {
          target[key] = source[key];
          seenKeys.add(key);
        }
        if (typeof source[key] === "object" && source[key] !== null) {
          recursiveMerge(target, source[key]);
        }
      }
    }
    recursiveMerge(target, source);
    return target;
  }
  // #########################################################



export default function Payments({ }) {
  // const [response, loading, error, axiosGet] = useAxiosFunction('GetPayment')
5




const onValueChange = async (e) => {
    await getBasket(simste,{ addpayment: e })
  }

  return (

    <div className='container h-min' >

      {(!payments) && 
      <div className={"absolute top-0 left-0 opacity-75 z-50 bottom-0 right-0 bg-white dark:bg-black justify-center items-center flex"}>
        {/* <Loading /> */}
      </div>
      }
      <>

        <div className='m-auto h-min max-h-[60vh] w-full min-w-[350px] min-h-[350px] overflow-auto container'>
          {/* <div className='flex flex-row flex-wrap gap-[15px] justify-around sm:justify-center'> */}
            <RadioGroup defaultValue={selpayment?.id} value={selpayment?.id} onValueChange={onValueChange} className='flex flex-wrap gap-[15px] justify-center' >
            {payments?.map((p) => {
              return (
                <Cards2 key={p.id} {...{ payments: payments, currency: currency, selpayment: selpayment, simste: simste, store: store, p: p }} />
              )
            })
            }
            </RadioGroup>
          {/* </div> */}
        </div>
      </>
    </div>
  )


}



function Cards({ currency, payments, selpayment, simste, store, p }) {


  const handleClick = async () => {
    if (selpayment?.id !== p?.id){
      const res = await getBasket(simste,{ addpayment: p?.id })

    } 
     
  }



  // 

  return (
    <div key={p.id} onClick={handleClick} className={cn('rounded-md flex flex-col relative justify-between items-start border \
                                    dark:border-primary border-neutral-300 min-w-[120px] cursor-pointer shadow-inner shadow-neutral-200 opacity-60 dark:opacity-50',
      (selpayment?.id === p?.id && 'ring-[3px] sm:ring-[5px] ring-green-600 ring-offset-1 opacity-100 dark:opacity-100'))}>
      <img src={p.image} className='rounded-t-md w-[120px] h-[55px]' />
      <div className='text-sm p-[0] flex flex-col justify-center items-center w-full'>
        {(p?.fee_rate > 0) && <small>fee {p?.fee_rate}%</small>}
        {(p?.fee_fix > 0) && <small>+ {p?.fee_fix} {currency?.sign}</small>}

        {(!(p?.fee_fix > 0) && !(p.fee_rate > 0)) && <small>free</small>}
      </div>
      {(selpayment?.id === p?.id) && <CircleCheckBig size={25}
        className='text-green-800 troke-[3px] sm:stroke-[3px] dark:text-green-500 absolute bottom-[0] right-[0] \
                                                             bg-primary rounded-full' />}
    </div>

  )


}

function Cards2({ currency, payments, selpayment, simste, store, p }) {
    
  return (
          <>
            <Label htmlFor={p.id} className="">
              <Card className={cn("@container/card relative cursor-pointer peer/nuts-[aria-checked]:bg-green-600 shadow-inner shadow-neutral-300 dark:shadow-neutral-800 dark:hover:bg-[#2A2A2A] hover:border-[#3A3A3A]",(selpayment?.id === p?.id && 'border-green-600 dark:bg-[#2A2A2A] hover:border-green-600')
              )}>
              <RadioGroupItem value={p.id} id={p.id} 
                              className="text-green-500 border-green-500 p-0 m-0 hidden aria-checked:block absolute left-[3px] bottom-[3px]" />
                <CardHeader className="p-[10px]">
                  {/* <CardDescription className="overflow-hidden max-w-[120px] break-words" >{p.name}</CardDescription> */}
                  <CardTitle className="p-0">
                    <img src={p.image} className='rounded-md w-[120px] h-[55px]' />
                  </CardTitle>
                  {/* <div className="absolute right-4 top-4">
                    <Badge variant="outline" className="flex gap-1 rounded-lg text-xs">
                      <TrendingUpIcon className="size-3" />
                      +12.5%
                    </Badge>
                  </div> */}
                </CardHeader>
                <CardFooter className="text-sm p-0">
                  <div className='text-sm p-[0] flex flex-col justify-center items-center w-full'>
                    {(p?.fee_rate > 0) ? <small>fee {p?.fee_rate}%</small>:<small>free</small> }
                    {(p?.fee_fix > 0) ? <small>+ {p?.fee_fix} {currency?.sign}</small>:<small className="text-transparent" >free</small>}
                  </div>
                </CardFooter>
              </Card>
            </Label>
          </>
  )
}
