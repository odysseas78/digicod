'use client'
export const dynamic = "force-dynamic";
import { Badge } from "@/components/ui/badge";
import wk from "@/lib/wk";
import {
  CircleCheckBig,
  LoaderPinwheel,
  Loader,
  PlusCircle,
  ShoppingCart
} from 'lucide-react';
import { useParams, usePathname, useRouter } from "next/navigation";
import { useEffect, useRef, useState, useTransition} from "react";
import { currencyFormat } from '@/app/checkout/helpers/functions'
// import { Button } from "@/components/ui/button"
import { cn } from '@/lib/utils'
import { defStore, simpleStore } from '@/store/zustand_1';
// import useContexData from '@/store/DefContext';




const refo = wk.refs
const $s = wk.signalP
$s.pricelabel = false
$s.rowid = undefined

function classNames(...classes) {
  return classes.filter(Boolean).join(' ')
}
// const ee = signal(document.querySelectorAll('[data-radix-popper-content-wrapper]'))

export default function PriceLabelDB(props) {
  // const { data, setContData } = useContexData();
  const { p, selected, setSelected, postBasket, cart } = props
  // const store = defStore()
  const simste = simpleStore()
  simste.pget(["cart"])?.products

  const router = useRouter()
  const params = useParams()
  
  // console.log(params)

  const [qty, setQty] = useState((simste.pget(["cart"])?.products && simste.pget(["cart"])?.products[p.id] && simste.pget(["cart"])?.products[p.id]?.qty) || 0)
  const popoverref = useRef(null)
  const pathname = usePathname()
  // const props = {
  //   cart:cart,
  //   selected:selected,
  //   setSelected:setSelected,
  //   qty:qty, 
  //   setQty:setQty
  // }

  const prp = {...props,qty,setQty}

  function hanleClick(e){
        setSelected(p)
  } 

  if(!cart?.currency?.shortname) return null
  const value = JSON.parse(p?.value)
  return (
    <div 
      // onClick={hanleClick}
      // onTouchStart={hanleClick}
      onPointerDown={(e) => {
        if(e.button === 0){
          // e.target.style.scale = 0.90
        }
      }} 
      onPointerUp={hanleClick} 
      className="relative notranslate"
       >
        {(simste.pget(["productloader"]) || simste.pget(["basketloader_addcur"])) && 
          <div className="absolute top-0 left-0 bottom-0 right-0 rounded-sm bg-background/60 backdrop-blur-[1px] z-30! grid place-items-center" ><Loader className="animate-spin w-5 rounded-full" /></div>}
      <Badge
        variant="outline"
        data-bdg={p?.id}
        className={cn('py-[20px] flex flex-row justify-between box-border rounded-md relative flex-1 gap-3 min-w-max! shadow-inner! shadow-neutral-300 dark:shadow-neutral-700! focus-within:border-neutral-600', 
        (selected?.id === p.id ? "ring-[1.5px]! dark:ring-[1.5px]! ring-green-600! dark:ring-green-500!":"cursor-pointer"))
        }>
        <Badge data-ss className={cn('min-w-max pointer-events-none flex flex-1 text-[0.80rem] sm:text-[0.90rem] py-[11.5px] box-border border-0 rounded-sm shadow-inner! shadow-neutral-500 dark:shadow-neutral-500!')} >
          {value.amount} {value.currency}
        </Badge>
        <Badge
          data-ff
          className={classNames('italic text-[0.80rem] sm:text-[0.90rem] min-w-max rounded-sm pointer-events-none py-[11.5px] shadow! shadow-neutral-300 dark:shadow-neutral-600')}
          variant="outline">
            {currencyFormat(p.price, cart.currency?.shortname)}
        </Badge>
        <div className="relative w-[35px]! flex justify-items-center-safe items-center">
            {simste.pget(["cart"]).products[p.id]?.qty > 0 ? 

            <div 
                className={cn("w-[25px]! h-[25px]! flex justify-center-safe items-center rounded-sm text-green-700! dark:text-green-500!", 
                ($s.rowid.value === p.id && simste.pget(["basketloader_addprod"]))  ? 'hidden':'')} >
              <ShoppingCart className={cn("w-full! h-full! flex-1 pointer-events-none")}  />
              <CircleCheckBig
                  className={cn("w-[23px]! h-[23px]! rounded-full! absolute! right-[-5px]! top-[-6px]! bg-background! pointer-events-none")} />
            </div>
            : 
            <div 
                className={cn("w-[25px] h-[25px] flex justify-center items-center active:scale-90 relative rounded-sm hover:[&>.vbn]:scale-110", 
                  ($s.rowid.value === p.id && simste.pget(["basketloader_addprod"]))  ? 'hidden':'', p.in_stock ? "cursor-pointer": "pointer-events-none" )}
                onPointerDown={(e) => {
                  if(e.button === 0){
                    // e.target.parentElement.style.scale = 0.95
                  }
                }} 
                onPointerUp={(e) => {
                  if(e.button === 0){
                    // e.target.parentElement.style.scale = 1
                    $s.rowid.value = p.id
                    postBasket(simste, { qty: 1, action:"add", product_id: p.id })
                    setQty(1)
                  }
                }} 
                >
                <ShoppingCart className={cn("w-full! h-full! flex-1 pointer-events-none")}  />
                <PlusCircle
                    className={cn("w-[25px]! h-[25px]! rounded-full absolute right-[-16px]! top-[-6px]! bg-background! vbn")} 
                />
            </div>
           }
           <LoaderPinwheel 
              className={cn("animate-spin absolute left-1 top-1/2 -translate-y-1/2 bg-background rounded-full", 
              ($s.rowid.value === p.id && simste.pget(["basketloader_addprod"]))  ? '':'hidden')}  size={30} />
        </div>
      </Badge>
    </div>
  )
}

