"use client"
import {
  CreditCardIcon,
  LogOutIcon,
  SettingsIcon,
  UserIcon,
  ShoppingBag, UserRoundCheck, UserRound, User, UserCheck, UserCheck2
} from "lucide-react"

import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/animate-ui/components/radix/dropdown-menu';
import Link from 'next/link';
import { AvatarIcon } from '@radix-ui/react-icons';
import { cn } from '@/lib/utils';
import { getCookies } from '@/lib/utils'
import { useEffect } from "react";
import { simpleStore, defStore } from '@/store/zustand_1';
import fetchActionClient from "@/app/actions/fetchActionBrowser";
import { useParams, useRouter, usePathname, useSearchParams } from "next/navigation";
import { SetCookies } from '@/app/actions/setcookies'
import wk from "../../lib/wk";



export function Dropdown({children}:any) {
  const simste = simpleStore()
  const router = useRouter()
  const usr = simste.pget(["usr_"])
  // wk.useClientLoadDebug("Dropdown")

    useEffect(()=>{
      const id = setTimeout(async () => {
          // simste.pset(['brandloader'], true)
        
          
        }, 0)
      return () => {
        clearTimeout(id)
      }
    },[])

  async function Logout(){
        const data = await fetchActionClient('LogOut', { })
        if(data?.detail === "Invalid token Error: HTTP 401") window.location.reload()
        const r = await SetCookies("delete", "auth_token", null)
        // router.refresh()
        // console.log(r);
        // router.push('/login')
        window.location.href = '/login'
  }

  useEffect(()=>{
    
  }, [])
  
  return (
    <>
      { usr === "true" ? <DropdownMenu>
        <DropdownMenuTrigger className="active:scale-90" asChild>
          <Button variant={"outline"} size={"icon-sm"} className="active:scale-90! border-green-500!" >
              {/* <UserRoundCheck className={cn('w-[1.8rem] h-[1.8rem] stroke-3 rounded-full active:scale-90 text-green-500')} /> */}
              <User className={cn('stroke-2! w-[1.2rem]! h-[1.2rem]! text-green-500')} />
          </Button>
          {/* <Button variant="outline">Open</Button> */}
        </DropdownMenuTrigger>
        <DropdownMenuContent>
          <Link href={"/account"} > 
            <DropdownMenuItem>
                <UserIcon />
              Profile
            </DropdownMenuItem>
          </Link>
          <Link href={"/account?c=orders"} > 
            <DropdownMenuItem >
                <ShoppingBag />
              Orders
            </DropdownMenuItem>
          </Link>
          <Link href={"/account?c=wallet"} > 
            <DropdownMenuItem>
              <img src={'/media/payment/dccoin.webp'} className='w-[17px] sm:w-[17px] rounded-md' />
              Wallet
            </DropdownMenuItem>
          </Link>
          {/* <DropdownMenuItem>
            <SettingsIcon />
            Settings
          </DropdownMenuItem> */}
          <DropdownMenuSeparator />
          <DropdownMenuItem onClick={(e:any)=>Logout()} variant="destructive">
            <LogOutIcon />
            Log out
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
      :
       <Link href={"/login"} > 
           <Button variant={"outline"} size={"icon-sm"} className="active:scale-90" >
              {/* <UserRoundCheck className={cn('w-[1.8rem] h-[1.8rem] stroke-3 rounded-full active:scale-90 text-green-500')} /> */}
              <User className={cn('stroke-[2px]! w-[1.2rem]! h-[1.2rem]!')} />
          </Button>
       </Link>}
    </>
    
  )
}
