"use client"
import React, { useEffect, useRef } from "react";
import { cn } from '@/lib/utils'
import {
    NavigationMenu,
    NavigationMenuContent,
    NavigationMenuItem,
    NavigationMenuLink,
    NavigationMenuList,
    NavigationMenuTrigger,
    navigationMenuTriggerStyle,
  } from "@/components/ui/navigation-menu"
import { useParams, useRouter } from 'next/navigation';
import fetchActionClient from "@/app/actions/fetchActionBrowser";
// import { signal } from "@preact/signals-core"
import { defStore, simpleStore } from '@/store/zustand_1'
import wk from "@/lib/wk";
import { Gift, CreditCard, TabletSmartphone, Smartphone } from "lucide-react";
import Link from 'next/link';


const s = wk.signalP
s.catbounce = 0
function setCookie(name, value, days = 365) {
    const expires = new Date(Date.now() + days * 864e5).toUTCString();
    document.cookie = `${name}=${value}; expires=${expires}; path=/; SameSite=Lax`;
}

export default function MenuBar({ fcategory }) {
    'use client'
    const params = useParams()
    const store = defStore()
    const simste = simpleStore()
    const isFirstRender = useRef(true)
    const router = useRouter()

    // wk.useClientLoadDebug("MyMenu")
    
    
    
    
    useEffect(() => {
       
  
        
        if(!store.region) store.dset(['region'], ['eu'])
            // fcategory?.length > 0 && store.dset(['categories'])
            // if (isFirstRender.current) {
            //     isFirstRender.current = false
            //     return
            //   }
            //   FetchAction(store)
           
          const id = setTimeout(async () => {
            //   const cats = await fetchActionClient("GetCategory", {})
              store.dset(['categories'], fcategory)
            //   console.log(s.catbounce.value)
            //   s.catbounce.value++
          }, 0)

        return () => {clearTimeout(id)} 
        
      }, [])


    // const categories = fcategory
    const categories = store.dget(["categories"]) || fcategory || []

    // const [selected, setSelected] = React.useState(store.catselected)
    // const handleChange = (e) => {
    //     setSelected(e)
    //     store.Set({ catselected: e })
    // }

    const dd = 1.4

    const rendr = (m) => {
        const caticons = {
            paymentcards: <CreditCard className={`w-[0.8rem]! sm:w-[0.9rem]!`} />, giftcards: <Gift className={`w-[0.8rem]! sm:w-[0.9rem]!`} />,
            mobile: <Smartphone className={`w-[0.8rem]! sm:w-[0.9rem]!`} />
        }
        return (

            <div key={m?.slug} className='flex! flex-row! z-50 items-center! justify-between! gap-1! h-full!'>
                {caticons[m?.slug]}
                <div translate="no" className='flex! text-[0.8rem] sm:text-[0.9rem] items-center! justify-center! p-0! m-0!' >{m?.name}</div>
            </div>

        )
    }

    // console.log(categories)

    return (
        <NavigationMenu className="w-full max-w-min h-full! max-h-min!">
            <NavigationMenuList className="w-full max-w-min gap-[0.4rem] h-full! max-h-min!">
                     {
                        categories && categories[0]?.id && categories?.map((c, i) => {
                            return (
                                <NavigationMenuItem key={c.id} className="w-full min-w-max h-full! max-h-min!">
                                    <NavigationMenuLink 
                                        asChild
                                        value={c?.slug} 
                                        className={cn("w-full min-w-max border rounded-sm px-[0.4rem]! py-1! focus:bg-transparent active:scale-[0.95]", 
                                        params.catslug === c.slug && "bg-accent focus:bg-accent")}>
                                            <Link key={c.id} 
                                                onNavigate={(e) => {
                                                    e.preventDefault()
                                                }}
                                                onPointerDown={(e) => {
                                                    if(e.button === 0){
                                                    // e.target.children[0].style.scale = 0.95
                                                    }
                                                }} 
                                                onPointerUp={(e) => {
                                                    if(e.button === 0){
                                                    // e.target.children[0].style.scale = 1
                                                    // handleChange(c.slug)
                                                    router.push(`/${c?.slug}`)
                                                    }
                                                }} 
                                            // className='w-full min-w-max z-50 cursor-pointer relative flex' 
                                                href={`/${c?.slug}`} >
                                                {rendr(c)}
                                        </Link>
                                    </NavigationMenuLink>
                                </NavigationMenuItem>
                                
                            )
                        })
                    }
                
            </NavigationMenuList>
        </NavigationMenu>


    )
}


