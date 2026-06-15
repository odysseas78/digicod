"use client"
import {
   Tabs,
   TabsContent,
   TabsContents,
   TabsList,
   TabsTrigger,
 } from '@/components/animate-ui/components/radix/tabs';
 import { Button } from '@/components/ui/button';
 import {
   Card,
   CardContent,
   CardDescription,
   CardFooter,
   CardHeader,
   CardTitle,
 } from '@/components/ui/card';
import { Badge } from "@/components/ui/badge"
 import { Label } from '@/components/ui/label';
 import {
   Table,
   TableBody,
   TableCaption,
   TableCell,
   TableHead,
   TableHeader,
   TableRow,
 } from "@/components/ui/table"
 import { mergeUniqueKeys, getCookie, currencyFormat } from './functions'
 import { initFingerprint } from '@/app/checkout/helpers/functions';
 import { defStore, simpleStore } from '@/store/zustand_1';
 import Link from 'next/link';
import { useParams, usePathname, useRouter, useSearchParams } from "next/navigation";
import React, { useEffect, useRef, useState, useTransition } from 'react';
import {
  Power,
  PowerOff,
  Loader,
  MoreVertical,
  LoaderPinwheel,
  ShoppingCart, CirclePower,
  CircleX, Plus, Minus, Trash, Trash2, CircleCheck
} from 'lucide-react';
import { Checkbox } from "@/components/ui/checkbox"
import wk from '@/lib/wk';
import { cn } from '@/lib/utils';
import Loading from '@/components/Loader'
import TooltipSimpl from '@/components/toltipSimpl'
import Payment from '@/components/Payment/Payment2'
import { TermsDialog, TermsDialog2 } from '@/components/SiteFooter/SiteFooter'
import TermsOofUse from '@/lib/TermOfUse/TermsConditions'
import PrivacyStatement from '@/lib/TermOfUse/privacy_statement'
import { Return_policy } from '@/lib/TermOfUse/return_policy'
import {
  Popover,
  PopoverTrigger,
  PopoverContent,
} from '@/components/animate-ui/components/radix/popover';
import { SimplDialog } from '@/components/Dialogs/MainDialog';
import { nanoid } from 'nanoid'
import fetchClient from '@/app/actions/fetchClient';
import Image from 'next/image'
import { djangoGet, djangoPostJson } from '@/app/actions/django-fetch-kit/next-server';
// import { MoonPayBuyWidget } from '@moonpay/moonpay-react';



function getCookies(name=null) {
    if (typeof document === 'undefined') return null;
    if(!name) return document.cookie;
      return document.cookie.split('; ').find(row => row.startsWith(name + '='))?.split('=')[1]
  }

function setCookie(name, value, days = 365) {
  const expires = new Date(Date.now() + days * 864e5).toUTCString();
  document.cookie = `${name}=${value}; expires=${expires}; path=/; SameSite=Lax`;
}

const refo = wk.refs
const $s = wk.signalP

$s.rowid = undefined
const word = "freecodecamp"


 export async function getBasket(simste, params) {
   "use client"
    // const stack = new Error().stack
    // console.log(stack)
   simste.pset(["basketloader"], true); simste.pset(["basketloader_addprod"], (params.addproduct ? true:false)); simste.pset(["basketloader_addcur"], (params.addcurrency ? true:false))
   const Data = await fetchClient("GET", "cart", null)

    simste.pset(["cart"], Data.cart)
   if(Data?.detail === "Invalid token Error: HTTP 401") window.location.reload()
// ###########  Dialog Messages #############################
    const id = setTimeout(() => {
      const id = nanoid()
      const capitalized = Data?.type?.charAt(0).toUpperCase() + Data?.type?.slice(1)
      if(Data.message) simste.pset(["simpldialogs", `${id}`], 
        <SimplDialog {...{title: capitalized, content: Data.message, type: Data.type, trigger: 1, fn: ()=>clearTimeout(id), id}} />)
     }, 0)
// ############# end Dialog Messages ###################3####
  //  const obb = structuredClone(simste.pget(["cart"]))
  //  mergeUniqueKeys(obb, Data.cart)
  //  simste.pset(["cart"], mergeUniqueKeys(obb,  Data.cart))
  
   setTimeout(()=>{
 
    simste.pset(["basketloader"], false); simste.pset(["basketloader_addprod"], (params.addproduct ? false:false)); simste.pset(["basketloader_addcur"], (params.addcurrency ? false:false))
  },350)
   }

 export async function postBasket(simste, params) {
      simste.pset(["basketloader"], true); simste.pset(["basketloader_addprod"], (params.addproduct ? true:false)); simste.pset(["basketloader_addcur"], (params.addcurrency ? true:false))
      // const Data = await fetchClient("POST", "cart", params)
      const Data = await djangoPostJson(`https://api.digicod.eu/cart/`, params)
      console.log(Data)
        simste.pset(["cart"], Data.cart)
    // ###########  Dialog Messages #############################
        const id = setTimeout(() => {
          const id = nanoid()
          const capitalized = Data?.type?.charAt(0).toUpperCase() + Data?.type?.slice(1)
          if(Data.message) simste.pset(["simpldialogs", `${id}`], 
            <SimplDialog {...{title: capitalized, content: Data.message, type: Data.type, trigger: 1, fn: ()=>clearTimeout(id), id}} />)
        }, 0)
    // ############# end Dialog Messages ###################3####
      setTimeout(()=>{
        simste.pset(["basketloader"], false); simste.pset(["basketloader_addprod"], (params.addproduct ? false:false)); simste.pset(["basketloader_addcur"], (params.addcurrency ? false:false))
      },0)
   }

 export default function Cart({basketdata, sendorder, setSendorder, fbasket, fcategory, fcurrency, ...props}){
  "use client"
   const pathname = usePathname()
   const store = defStore()
   const simste = simpleStore()
   const smget = simpleStore().pget
   const smset = simpleStore().pset
  //  const cart = mergeUniqueKeys(structuredClone(simste.pget(["cart"])), basketdata?.cart)
  const simstebasket = simste.pget(["cart"])?.id && simste.pget(["cart"])
   const cart = simstebasket || fbasket?.cart
   const router = useRouter()
   const fref = useRef()
   const params = useParams()
   const searchparams = useSearchParams()

   const [IsClient, setIsClient] = useState(false)


  useEffect(() => {
   setIsClient(true)
  
}, [])



  //  console.log(simste.pget(["cart"])?.id)
  // typeof document !== 'undefined' && simste.pget(["cart"])?.id && setCookie('_ccc', simste.pget(["cart"])?.id)
   const isFirstRender = useRef(true)
   useEffect(() => {
    // (simste.pget(["cart"])?.id || cart?.id) && setCookie('_ccc', (simste.pget(["cart"])?.id || cart?.id))
    // initFingerprint()
      simste.pset(["getBasket"], getBasket)
       if (isFirstRender.current && !props.minicart) {
          //  const id = setTimeout( async () => {
          getBasket(simste, {})
          //  console.log(pathname);
        // }, 500)
          isFirstRender.current = false
        }
       
   
      return () => {
          // clearTimeout(id)
      }
    }, [])
    // if(!IsClient) return
   if(props.minicart) return MiniCart({ cart, simste, router })
    
   return (
          <BasketTabs {...{ cart, simste, params, store, router, pathname, setSendorder }} />
   )
 }





 function BasketTabs({ cart, simste, params, store, router, pathname, setSendorder }) {
  "use client"
  const tabvalues = ["cart", "payment"]
  const searchparams = useSearchParams()
  const termsref = useRef()
  const cb = searchparams.get('c')
  const c = (pathname === '/checkout') ? (tabvalues.filter((f)=>f===cb)[0] ? cb : tabvalues[0]): tabvalues[0]
  const defaultValue = "cart"
  const basketloader = simste.pget(["basketloader"])
  const [tabsval, setTabsval] = useState(c)
  useEffect(()=>{
    (pathname === '/checkout') && setTabsval(c)
  },[c])

 



   return (
     <div className="flex w-full! flex-col gap-2 min-w-min p-0 mb-1 relative rounded-md">
      {/* ########### coinwallet payment toggle ############# */}
      {(simste.pget(['usr_']) === 'true') && 
      pathname === '/checkout' && tabsval === 'payment' &&
          <div className='absolute top-0 right-px' >
              <ToggleWalletPayment {...{ basketloader }} />
          </div>}
      {/* ########### coinwallet payment toggle ############# */}
       <Tabs 
          defaultValue={tabsval} 
          value={tabsval} 
          onValueChange={(e)=> {
            setTabsval(e)
            router.replace('/checkout?c='+e)
          } } 
          className='p-0! m-0! rounded-md! text-xs! sm:text-sm!'>
         {pathname === '/checkout' && <TabsList className='text-xs! sm:text-sm!'>
           <TabsTrigger value={tabvalues[0]}>cart</TabsTrigger>
           <TabsTrigger disabled={cart?.total_products === 0} value={tabvalues[1]}>Payment</TabsTrigger>
         </TabsList>}
         <Card className="p-0! m-0! w-full! rounded-md">
    
           {/* {simste.pget(["basketloader"]) && <Loading position={"absolute"} opacity='opacity-20'  />} */}
           <TabsContents className="px-0! py-0! my-0! mx-0! w-full!">
            <Tab_1 {...{cart, simste, store, router, params, tabsval}} />
            <Tab_2 {...{cart, simste, store, router, params, tabsval, setSendorder, termsref}} />
            
             {/* ///////////////////////////////////////// */}
           </TabsContents>
         </Card>
        
       </Tabs>
     </div>
   );
 }



import { Toggle } from "@/components/ui/toggle"
import { boolean } from 'zod';

export function ToggleWalletPayment({ basketloader }) {
  const simste = simpleStore()
  const cart = simste.pget(['cart'])
  const togglewallet = simste.pget(['togglewallet'])
  const isFirstRender = useRef(true)
  // console.log(!(!togglewallet))


  return (
    <Toggle 
      pressed={!(!Number(cart.wallet_payment))} 
      onPressedChange={(e)=>getBasket(simste, {wallet:e})} 
      aria-label="Toggle dcoins" size="xs" variant="outline"
      className={cn('text-xs! rounded-sm p-[5px] data-[state=on]:ring-green-500! data-[state=on]:ring-2! data-[state=off]:grayscale!', 
        'active:scale-95 data-[state=on]:shadow-inner! shadow-neutral-300! dark:shadow-neutral-500!', 
        'flex items-center')}
      disabled={simste.pget(['usr_']) === 'false' || basketloader}
      >
      {/* Use<img src={'/icons/dcoin_1.svg'} className='rounded-full w-[25px]' />coins */}
      Use<Image src={'/media/payment/dccoin.webp'} alt='Dcoin' width={18} height={18} />coins
       <Power className='w-[21px]! h-[21px]! group-data-[state=off]/toggle:hidden text-green-500 stroke-3! font-bold!' />
       <PowerOff  className='group-data-[state=on]/toggle:hidden w-[21px]! h-[21px]!' />
    </Toggle>
  )
}


function Tab_2({cart, simste, store, tabsval, router, setSendorder,  termsref}){
  "use client"
  const [checked, setChecked] = useState(false)
  const subtotal = cart?.currency?.shortname && currencyFormat(cart?.total_price, cart?.currency?.shortname)
  const fee = cart?.currency?.shortname && currencyFormat(cart?.process_fee, cart?.currency?.shortname)
  const total = cart?.currency?.shortname && currencyFormat(cart?.final_price, cart?.currency?.shortname)
  const wallet_payment = !(!cart?.wallet_payment) && currencyFormat(cart?.wallet_payment, cart?.currency?.shortname)
  const subtotal2 = cart?.currency?.shortname && currencyFormat((Number(cart?.total_price) - Number(cart?.wallet_payment)), cart?.currency?.shortname)
   const coinWallet = simste.pget(["coinWallet"])

  // console.log(Number(wallet_payment))
  const dcoins = (Number(cart?.wallet_payment) / Number(cart?.currency?.price) * 33).toFixed(0)

  useEffect(()=>{setChecked(false)},[tabsval])
 
  return (
    <TabsContent value="payment" className="w-full! py-3! sm:py-4! text-xs! sm:text-sm!">
      {/* {(!simste.pget(["cart"])loader) && <Loading />} */}
      <CardContent className="px-5! sm:px-[15px]!">
        <div className={'flex flex-row justify-between w-full! py-[5px]'}>
          <div className='flex h-[50px] sm:h-[55px]'>
            {cart?.payment_method?.name === "Wallet" ? <img src={cart?.payment_method?.image} className='w-[50px] sm:w-[55px] rounded-md' />
            :
            <img src={cart?.payment_method?.image} className='w-[100px] sm:w-[120px] rounded-md' />}
          </div>
          
          


          <div className='text-right font-normal flex flex-col justify-end text-xs! sm:text-sm!'>
            <Table className="">
              <TableBody className="text-xs! sm:text-sm!">
                <TableRow className='hover:bg-transparent! pointer-events-none! border-none!' >
                  <TableCell className="font-medium py-[1px]!">Subtotal:</TableCell>
                  <TableCell className="py-0!">{subtotal}</TableCell>
                </TableRow>

                {(!(!Number(cart?.wallet_payment)) && (simste.pget(['usr_']) === 'true')) && 
                <>
                <TableRow className='hover:bg-transparent! pointer-events-none!'>
                  <TableCell className="font-medium flex justify-end gap-[5px] items-center py-[1px]!">
                    <div>- {dcoins}</div>
                     <img src={'/media/payment/dccoin.webp'} className='w-[14px]' />:
                  </TableCell>
                  <TableCell className="py-0!">- {wallet_payment}</TableCell>
                </TableRow>
                <TableRow className='hover:bg-transparent! pointer-events-none! border-none!' >
                  <TableCell className="font-medium py-[1px]!">Subtotal:</TableCell>
                  <TableCell className="py-0!">{subtotal2}</TableCell>
                </TableRow>
                </>}

                <TableRow className='hover:bg-transparent! pointer-events-none!'>
                  <TableCell className="font-medium py-[1px]!">Fee:</TableCell>
                  <TableCell className="py-0!">{fee}</TableCell>
                </TableRow>
                <TableRow className='hover:bg-transparent! pointer-events-none!'>
                  <TableCell className="font-medium">Total:</TableCell>
                  <TableCell className="">{total}</TableCell>
                </TableRow>
                
              </TableBody>
            </Table>
            {/* {!(!Number(cart?.wallet_payment)) && 
            <div className='flex flex-row justify-end'>
              <div className='text-right w-full flex! gap-1 justify-around items-center' >
                <img src={'/media/payment/dccoin.webp'} className='w-[18px]' />
                <div>- {dcoins} Dcoins:</div>
              </div>
              <div className="text-right min-w-[70px] text-nowrap" >- {wallet_payment}</div>
            </div>} */}
          </div>

        </div>

        <div className="flex flex-col items-center w-full! mt-[10px]">
          <div className="flex flex-row justify-start items-start space-x-2 w-full!">

            <Checkbox className='mt-[3px]' required checked={checked} onCheckedChange={(e) => setChecked(e)} id="terms2" disabled={false} />
            <label className="text-xs text-wrap flex flex-row flex-wrap font-medium peer-disabled:cursor-not-allowed p-0! m-0! peer-disabled:opacity-70"
            htmlFor="terms2">
              
              <div className="text-xs font-normal text-wrap flex-wrap flex flex-row w-full">
                  <div>
                    I have read and agree to Digicod&nbsp;
                    <TermsDialog content={<TermsOofUse />} title="Terms of use" >
                    <i className='underline font-bold cursor-pointer'>Terms & Conditions</i>
                    </TermsDialog>,&nbsp;
                    <TermsDialog content={<PrivacyStatement />} title="Privacy Policy" >
                      <i className='underline font-bold cursor-pointer'>Privacy Policy</i>
                    </TermsDialog>,&nbsp;
                    <TermsDialog content={<Return_policy />} title="Return Policy" >
                      <i className='underline font-bold cursor-pointer'> Return Policy</i>
                    </TermsDialog>.
                    I accept the purchase and direct delivery
                    of non-refundable goods and waive my right of withdrawal.
                  </div>
                </div>
            </label>
          </div>
          
          <div className='my-[15px] pt-[5px] w-full! text-center'>
            <Button 
                type='button' 
                variant="default" 
                size="sm"
                onPointerDown={(e)=>{
                  if(e.button === 0){
                    // setSendorder(true)
                  // store.Set({sendorder:true})
                  // router.replace('/checkout?c=sendorder')
                  }
                  
                }}
                onPointerUp={(e)=>{
                  if(e.button === 0){
                    // setSendorder(true)
                    store.dset(['sendorder'], true)
                    router.replace('/checkout?c=sendorder')
                  }
                  
                }}
                disabled={!checked}
                className='active:scale-95 hover:scale-105 shadow-inner! shadow-neutral-300 dark:shadow-neutral-950 rounded-md'>
              Please order | <b className='pointer-events-none'><i>{total}</i></b>
            </Button>
          </div>
        </div>

        

        <div className="max-h-[30vh]! w-full! overflow-y-auto mt-[10px]! pr-[7px]! mx-0">
          <Payment />
        </div>
        
      </CardContent>

    </TabsContent>
  )
 }

 function Tab_1({cart, store, params}){
  "use client"
  const router = useRouter()
  const pathname = usePathname()
  const simste = simpleStore()
  const basket2 = simste.pget(["cart"])?.id ? simste.pget(["cart"]) : cart
  
  
  if(basket2?.total_products === 0 && pathname === '/checkout') setTimeout(()=>{router.replace('/')}, 1000)

   return (
      <TabsContent value="cart" className="sm:pl-3! mt-1! px-0! mx-0!">
         {/* <CardHeader> */}
         {/* <CardTitle>cart</CardTitle> */}
         {/* <CardDescription>
            Make changes to your account here. Click save when you&apos;re
            done.
         </CardDescription> */}
         {/* </CardHeader> */}
         <CardContent className="px-0! mx-0!">
        { cart?.total_products > 0 ? 
        <div className="py-3!">
         <Table className='px-0! mx-0!'>
            {/* <TableCaption>A list of your recent invoices.</TableCaption> */}
            <TableHeader className='font-mono text-[clamp(0.7rem,1vw,0.85rem)]!'>
               <TableRow>
                  <TableHead className="w-full">Product</TableHead>
                  <TableHead className="text-right w-[60px]">Qty</TableHead>
                  <TableHead className="text-right w-[60px]">price</TableHead>
                  <TableHead className="text-right w-[60px]">Total</TableHead>
                  <TableHead className="text-right w-[30px] p-0 m-0"></TableHead>
               </TableRow>
            </TableHeader>
            <TableBody className='text-[clamp(0.7rem,1vw,0.85rem)]!'>
               {
                
                 basket2.products.map((p)=>{

                              const d = basket2.products[p.id]
                     return (
                        <TableRow key={p.id} ref={refo[`${p.id}`]} className={cn('relative')}>
                           <TableCell className="wrap-anywhere overflow-hidden max-w-[150px]">
                            {(simste.pget(["productloader"]) || simste.pget(["basketloader_addcur"])) && 
                              <div className="absolute top-0 left-0 bottom-0 right-0 rounded-sm bg-background/80 backdrop-blur-[1px] z-30! grid place-items-center" >
                                <Loader className="animate-spin w-5 rounded-full" /></div>}
                              <LinkWrap {...{ p, params, simste, store, router}} >
                              {p.title}
                              </LinkWrap>
                              </TableCell>
                           <TableCell className="text-right w-[60px] relative">
                              {d?.qty}
                            <LoaderPinwheel className={cn("animate-spin absolute left-[60%] top-1/2 -translate-y-1/2", (simste.pget(["basketloader_addprod"]) && $s.rowid.value === p.id)  ? '':'hidden')}  size={25} />
                            </TableCell>
                           <TableCell className="text-right w-[60px]">{currencyFormat(p?.item_price, basket2.currency.shortname)}</TableCell>
                           <TableCell className="text-right w-[60px]">{currencyFormat(p?.final_price, basket2.currency.shortname)}</TableCell>
                           <TableCell className="text-right! w-[30px] pr-0!"><CellDropdown {...{ p, simste }} /></TableCell>
                        </TableRow>
                     )
                  })
               }
            </TableBody>
            </Table>
            <div className='w-full border-t px-[5px] text-[0.8rem]! py-5! sm:text-[0.9rem]! flex flex-row justify-between items-center!'>
             { 
              <Button 
                variant="outline"
                size="sm"
                className='cursor-pointer hover:scale-[1.05] active:scale-[0.95] relative'
                onPointerUp={(e)=>{
                  if(e.button === 0){
                    // setSendorder(true)
                    store.Set({sendorder:true})
                    router.push('/checkout?c=payment')
                  }
                }}
                >
                  Checkout
              </Button>
              }
               <div className='text-right font-normal mr-[35px] flex flex-row gap-[20px] justify-end items-center'>
                  <div>Total:</div>
                  <div className='font-bold'>{basket2?.currency?.shortname && currencyFormat(basket2?.total_price, basket2?.currency?.shortname)}</div>
               </div>
            </div>
         </div>
         :
         <div className='w-full h-[250px] flex justify-center items-center'>
              cart IS EMPTY
          </div>
          }
         </CardContent>
         
      </TabsContent>
   )
 }

 const LinkWrap = ({children, p, params, store, router, simste}) =>{

   return (
      <div className='w-full text-wrap' >
         <Link
            replace={false}
            scroll={false}
            href={{
               pathname:`/${p.brand?.category[0].slug}/${p.brand?.slug}`, query: { r: p.region } }}
               onNavigate={(e) => {
                  e.preventDefault()
               }}
               // className='cursor-pointer'
               onPointerDown={(e) => {
                if(e.button === 0){
                  e.target.style.scale = 1.05
                }
              }}
              onPointerUp={(e) => {
                if(e.button === 0){
                  e.target.style.scale = 1.0
                  router.push(`/${p.brand.category[0].slug}/${p.brand.slug}?r=${p.region}`)
                  
                } 
              }}
            className={cn(((p.brand?.slug !== params?.brandslug) || ((p.brand?.slug === params?.brandslug) && (p.region !== store.dget(['region'])[0]))) ?
               'flex underline w-max' : 'pointer-events-none')}  >
            {children}
         </Link>
      </div>
   )
 }


function ButtonRounded({icon, simste, p}) {
  "use client"
   const res = icon === 'plus' ? <Plus className='w-full m-0 pointer-events-none' width={300} />:
   icon === 'minus' ? <Minus className='w-full m-0 pointer-events-none' width={300} />:
   icon === 'remove' ? <Trash2 className='w-full m-0 pointer-events-none text-red-500' width={300} />:''
  return (
    <div className="flex flex-row">
      <Button  
          onPointerDown={(e) => {
            if(e.button === 0){
            }
          }}
          onPointerUp={(e) => {
            if(e.button === 0){
              if(icon === 'plus') postBasket(simste, { action:"add", qty: (simste.pget(["cart"])?.products[p.id]?.qty || 0) + 1, product_id: p.product.id })
              if(icon === 'minus' && p?.qty > 0) postBasket(simste, { action:"add", qty: simste.pget(["cart"])?.products[p.id]?.qty - 1, product_id: p.product.id })
              if(icon === 'remove' && p?.qty > 0) postBasket(simste, { action: "remove", product_id: p.product.id })
            } 
          }}
         disabled={simste.pget(["basketloader"])}
         variant="outline" 
         size="icon-sm" 
         className="rounded-full flex transition-all duration-50 active:scale-90 p-0 pointer-events-auto bg-card! cursor-pointer shadow! shadow-neutral-300 dark:shadow-neutral-700 hover:scale-105">
       {res}
      </Button>
    </div>
  )
}


function toggleClaslist(elclslist,clsList){
  for (const cls of  clsList){
     elclslist.toggle(cls)
  }
}

 function CellDropdown({p, simste}){
    const [isOpen, setIsOpen] = useState()
    const [pointerDown, setPointerDown] = useState(false)
    const triggerref = useRef()

    const events = ['pointerdown']
   return (
     <Popover 
      open={isOpen}
      modal={true}
      onOpenChange={(e)=>{
        setIsOpen(e)
        if(e){
          $s.rowid.value = p.id
          toggleClaslist(
            refo[`${p.id}`]?.current?.classList, 
            ['bg-secondary', 'shadow-inner', 'shadow-neutral-400', 'dark:shadow-neutral-600', 'rounded-sm']
          )
        } else {
          toggleClaslist(
            refo[`${p.id}`]?.current?.classList, 
            ['bg-secondary', 'shadow-inner', 'shadow-neutral-400', 'dark:shadow-neutral-600', 'rounded-sm']
          )
        }
      }}>
       <PopoverTrigger 
          className='ring-0! w-full! h-full! focus-visible:ring-0! flex! focus:ring-0! justify-center! min-h-max items-center! active:ring-0! cursor-pointer active:border-0! focus-visible:border-none! focus:border-0! relative!'
          >
         {/* <div>DDD</div> */}
         <div className='' ><MoreVertical className='m-0! p-0!' /></div>
       </PopoverTrigger>
       <PopoverContent 
          align="end" 
          side='top' 
          transition={{ type: 'spring', stiffness: 2500, damping: 100 }}
          sideOffset={12} 
          className="flex gap-3 flex-row p-[0.6rem] w-min justify-cente items-center bg-secondary! mr-0 shadow-inner! shadow-secondary/50 dark:shadow-neutral-600!">
         {/* <img src={p.image} className='w-[50px] h-[50px] rounded-md' /> */}
         <ButtonRounded simste={simste} p={p} icon='minus' />
         <ButtonRounded simste={simste} p={p} icon='plus' />
         <ButtonRounded simste={simste} p={p} icon='remove' />
       </PopoverContent>
     </Popover>
   )
}

function MiniCart({ cart, simste, router }){
  "use client"
  // const pathname = usePathname()
  // const store = defStore()
  // const simste = simpleStore()
  const basket2 = simste.pget(["cart"])?.id ? simste.pget(["cart"]) : cart
  // const router = useRouter()
  // const fref = useRef()
  // const params = useParams()
  const riconssize = 25
  useEffect(()=>{getBasket(simste, {})}, [])

  return (
    <Link 
      href={basket2?.total_products && basket2?.total_products > 0 ? `/checkout?c=cart` : ''} 
      onNavigate={(e) => {
        e.preventDefault()
      }}
      onPointerDown={(e) => {
        if(e.button === 0){
          e.target.children[0].style.scale = 0.8
        }
      }}
      onPointerUp={(e) => {
        if(e.button === 0){
          setTimeout(()=>{
            e.target.children[0].style.scale = 1
          },70)
          basket2?.total_products && basket2?.total_products > 0 && router.push(`/checkout?c=cart`)
        }
      }} 
      className={cn('block p-0 m-0', !(basket2?.total_products && basket2?.total_products > 0) && 'pointer-events-none')}
      >
      <div ref={refo.minicart} className='relative pointer-events-none' >
        <ShoppingCart size={riconssize} className='pointer-events-none' />
        <div className={cn('absolute top-[-8px] right-[-11px] bg-green-800 text-white! text-bold text-[13px]! p-[2px]!', 
          'w-[18px]! h-[18px]! flex! flex-row! justify-center! items-center! rounded-full pointer-events-none', !(basket2?.total_products > 0) && "bg-neutral-700")} >
          {(basket2?.total_products ?? 0)}
        </div>
      </div>
    </Link>
  )
}

