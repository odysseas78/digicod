'use client';
export const dynamic = "force-dynamic";
import { AvatarIcon, MoonIcon } from '@radix-ui/react-icons';
import React, { useEffect, useMemo, useRef, useState } from "react";
import { simpleStore, defStore } from '@/store/zustand_1';
// import LoginModal from '../../components/Auth/LoginRegister/LoginModal';
// import TodoList from '../MyAccount/Table/TableCls'
import useWindowSize from "@/hooks/UseWindowSize";
import wk from '@/lib/wk';
import { useParams, useSearchParams, useRouter } from "next/navigation";
import { Button } from '@/components/ui/button';
import fetchClient from '@/app/actions/fetchClient';
import {testAction} from '@/app/actions/test';
import { create } from 'zustand'
import Link from 'next/link';
import { regionCalc } from '@/app/(products)/[catslug]/ProductList'
import { encrypt, decrypt } from '@/lib/xorCipher'
import Loading from '@/app/loading'
import { AlertDialogDestructive } from '@/components/Dialogs/AlertDialog'
import { FormExample } from '@/components/FormExample';
import DefaultDataTable from '@/app/(protrcted)/account/Tables/DefaultDataTable'
import {
   Tabs,
   TabsContent,
   TabsContents,
   TabsList,
   TabsTrigger,
 } from '@/components/animate-ui/components/radix/tabs';
  import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
  } from '@/components/ui/card';
import { tableStore } from '@/app/(protrcted)/account/tablestore'
import { AnimatePresence, LayoutGroup, motion } from "framer-motion";
import { ClientLoadProbe, useClientLoadDebug } from '../../lib/DebugInstrumenty';
import { djangoPostJson, djangoGet } from '../actions/django-fetch-kit/next-server';



 const html = []
function useDeviceInfo() {
  // const [devinfo, setDevinfo] = useState([])
 
  const info = {};
  // Basic Browser & System Info
  info.userAgent = navigator.userAgent;
  info.platform = navigator.platform;
  info.language = navigator.language;
  info.online = navigator.onLine ? "Online" : "Offline";
  // Screen Info
  info.screenWidth = screen.width;
  info.screenHeight = screen.height;
  info.orientation = screen.orientation ? screen.orientation.type : "Unknown";
  // Network Info
  if ('connection' in navigator) {
    const connection = navigator.connection;
    info.connectionType = connection.effectiveType;
    info.downlink = connection.downlink + " Mbps";
    info.rtt = connection.rtt + " ms";
  } else {
    info.connectionType = "Not supported";
  }
  // Battery Info
  // if ('getBattery' in navigator) {
  //   const battery = await navigator.getBattery();
  //   info.batteryLevel = (battery.level * 100) + "%";
  //   info.charging = battery.charging ? "Yes" : "No";
  // } else {
  //   info.batteryLevel = "Not supported";
  // }
  // Device Memory
  info.memory = navigator.deviceMemory ? navigator.deviceMemory + " GB" : "Unknown";
  info.devicePixelRatio = window.devicePixelRatio ? window.devicePixelRatio : "Unknow"
  info.maxTouchPoints = navigator.maxTouchPoints ? navigator.maxTouchPoints : "unknown"
  // Geolocation
  if ('geolocation' in navigator) {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        info.latitude = pos.coords.latitude;
        info.longitude = pos.coords.longitude;
        logDeviceInfo(info);
      },
      (err) => {
        info.locationError = err.message;
        logDeviceInfo(info);
      }
    );
  } else {
    info.location = "Not supported";
    logDeviceInfo(info);
  }
return info
}
// Function to display info neatly
function logDeviceInfo(info) {
  console.log("=== DEVICE INFO DASHBOARD ===");
  for (const [key, value] of Object.entries(info)) {
    // html.push(<div><span>{`${key}: `}</span><span>{`${value}`}</span></div>)
    console.log(`${key}:`, value);
  }
  console.log("============MY DEVICE INFO SHOWN ON THE BROWSER=================");
}

const tabledata =(data)=> {
  return data.map((m)=>{
  
      m.Date = m.created_at,
      m.Total = m.total.b,
      m.Currency = m.cart.currency.shortname,
      m.Payment = m.cart.payment_method.name,
      m.Status = m.status
    return m
  })
}
// function getCookie(name=null) {
//   if (typeof document === 'undefined') return null;
//   if(!name) return document.cookie;
//     return document.cookie.split('; ').find(row => row.startsWith(name + '='))?.split('=')[1]
// }

const refo = wk.refs
// const $s = wk.signalP

// const useStore = create((set) => ({
//   storSet: (data) => set((state) => {
//       return({...state,...data})}),
// }))

function Collapse({children, trigger}){
  const [open, setOpen] = useState()
  const collapsref = useRef()
  const simste = simpleStore()
  // const trigger = simste.pget([name])
  

  useEffect(()=>{
  // console.log(trigger)
  const clsList = collapsref.current?.classList
  // console.log(trigger)
  // simste.set((prev)=>{
  //    // console.log(prev)
  //    const h = {...prev}
  //    h.collap[p.id] = clsList

  //    return {...h}})
  if(clsList){
    if(clsList.contains('grid-rows-[1fr]!')){
      clsList.toggle('grid-rows-[0fr]!')
      clsList.toggle('grid-rows-[1fr]!')   
      setOpen(false)   
  } else {
    clsList.toggle('grid-rows-[1fr]!')
    clsList.toggle('grid-rows-[0fr]!')
    setOpen(true)
  }
  }

  // const gg = simste.collap
  //    gg && console.log(gg)
  //    for (const l of Object?.keys(gg)){

  //       if(Number(l) !== Number(trigger[0]) && gg[l].contains('grid-rows-[1fr]!')){
  //          gg[l].toggle('grid-rows-[0fr]!')
  //          gg[l].toggle('grid-rows-[1fr]!')
  //       }
  //    }
  },[trigger])


  //  return children

  return (
    <div ref={collapsref} className="grid! grid-cols-1 grid-rows-[1fr]! overflow-hidden! m-0! p-0! transition-all duration-700 max-w-full">
      <div className='min-h-0'>
        {children}
      </div>
    </div>
  )
}


export default function Homepage({}) {
  const [st, setSt] = useState()
  // const us = wk.useStateProxy(undefined, setSt)
  const store = defStore()
  const ss = wk.storeProxy(undefined, defStore())
  const simste = simpleStore()
  const sm = wk.simProxy(undefined, simpleStore())
  const cart = simste.pget(['cart'])
  
  // const searchparams = useSearchParams()
  // const modal = simplestore
  // const [modals, setModals] = useState([])
  const [data, setData] = useState(false)
  const [loading, setLoading] = useState(false)
  const params = useParams()
  // const user = store.user
  const router = useRouter()
  const tbstore = tableStore()
  

// wk.useClientLoadDebug("Home")

  
// console.log(sm)


      useEffect(()=>{
        const id = setTimeout(async () => {
          setLoading(true)
            const Data = await fetchClient('GET', "brand")
            if(Data?.detail === "Invalid token Error: HTTP 401") window.location.reload()
            setData(Data)
            Data && simste.pset(["prodlist"], Data)
            store.dset(["brands"], Data)
            setLoading(false)
          }, 0)
       
        return () => {
          clearTimeout(id)
        }
      },[])



  
// const [state, action, pending] = useActionState(getUserServer, undefined)

  async function ftch() {
    const res = await fetch('api/orders')
    // const res = await fetchActionClient('LoginRegister', {filter:{'email':'coxah@web.de'}})
    // const res = await fetchActionClient('url', {url: 'https://front.digicod.eu/rest/api/orders/'})
    // const res = await fetch("https://front.digicod.eu/api/custom-login-verify/?token=TeYCtlGIYLu0saIfwCMTBQS68yxKgQqE346ruunYYpa4yqbY1x&email=coxah%40web.de")
    // const res = await fetch("https://front.digicod.eu/api/custom-login-verify/?token=TeYCtlGIYLu0saIfwCMTBQS68yxKgQqE346ruunYYpa4yqbY1x&email=coxah%40web.de")
     console.log(await res.json());
    return res
  }




 const region = simste.pget(['regionCalc'])

 const [IsClient, setIsClient] = useState(false)

// const test1bbb = simste.pget(['test1', 'bbb'])

//  useEffect(() => {

//   console.log('us',us)
//   // console.log(simste)
//   }, [us])

//   useEffect(() => {

//   console.log('us.gg',us.gg)
//   // console.log(us)
//   }, [us.gg])
//    useEffect(() => {

//   console.log('us.ss',us.ss)
//   // console.log(us)
//   }, [us.ss])

//    useEffect(() => {
    
//      console.log('uu.a',sm.uu.a)
//   }, [sm.uu.a])

//      useEffect(() => {
//     console.log('cart', sm.cart)

//   }, [cart])

//   const imageBase64 = fs.readFileSync('public/logos/dclast_b.svg', { encoding: 'base64' });
// const dataUrl = `data:image/svg;base64,${imageBase64}`;



 useEffect(() => {
  setIsClient(true)

}, [])

if(!IsClient) return null

function myQuerySelectAll(el, array=false){
   const els = typeof document !== 'undefined' ? document.querySelectorAll(el) : undefined
   return array ? Array.from(els) : els
}

// const iframe = myQuerySelectAll('iframe')
// console.log(iframe)

// Source - https://stackoverflow.com/a/64976943
// Posted by Cary Meskell, modified by community. See post 'Timeline' for change history
// Retrieved 2026-04-18, License - CC BY-SA 4.0

function querySelectorAllInIframes(selector) {
  let elements = [];

  const recurse = (contentWindow = window) => {

    const iframes = contentWindow.document.body.querySelectorAll('iframe');
    iframes.forEach(iframe => recurse(iframe.contentWindow));
    
    elements = elements.concat(contentWindow.document.body.querySelectorAll(selector));
  }

  recurse();

  return elements;
};

function access() {
   const iframe = typeof document !== 'undefined' ? document.querySelectorAll("iframe")[0]:undefined
   const innerDoc = iframe ? iframe.contentDocument || iframe.contentWindow?.document : undefined
  //  console.log(iframe?.innerHTML);
   iframe && console.log(iframe.contentDocument['#dokument']);
   iframe && console.log(iframe.contentWindow);
}

IsClient && access()

const c = wk.signal(false)
if(!IsClient || loading || !data) return <Loading />
  return (

    <div className='z-0'>
      <div className='flex flex-col' >
        <Button className='hero' onClick={async function (e){
        // const Data = await fetchActionClient('GetBasket', {wallet:'toggle'})
            // simste.pset(["collapse"], (simste.pget(["collapse"]) ? simste.pset(["collapse"]) + 2 : 3))

      //  sm.uu = {a:4,b:8,c:0}
    
        
        }} >AAA</Button>
   
         <Button onClick={async function (e){
          // const gg = await testAction("client.GET('dost')")
          // router.refresh()
          // simste.pset(['test1'], 444)
        //  const Data = await fetchActionClient('GetBasket', {})
            const res = await djangoPostJson("https://front.digicod.eu/api/cart/", {action:"add", qty:1, product_id:3330})
            // const res = await djangoGet("https://front.digicod.eu/api/cart/")
                  const data = await res

           console.log(res)
        }} >BBB</Button>
        <div className='p-[5px]'>
          <div className='flex justify-center text-[1.5rem] font-semibold gert' >
            Your shop for digital goods
          </div>
        </div>
        <AlertDialogDestructive />
        <Collapse trigger={simste.pget(['trgr1'])} >
        <div className='flex flex-row flex-wrap justify-center' >
          {
           data && data?.length > 0 && data.filter((d)=>d.image2).map((b)=>{
            const reg = regionCalc(b, store, cart)
        
              return (
                <Link className='flex' key={b.id} href={{ pathname: `/${b.category[0].slug}/${b.slug}`, query: {r: (reg || b.regions[0])} }} >
                      <img src={b.image2} title={b.title} className='w-8 sm:w-12 m-[6px] rounded-md flex' />
                </Link>
              )
            })
          }
        </div>
        </Collapse>

        {/* <div className='flex'>
          <div className='flex justify-center w-full p-[5px]' >
            <img src='/media/def/giftcards.png' />
          </div>
        </div> */}
        {/* {
      
         devinfo &&  Object.keys(devinfo).map((t)=>{
           return (
            <div key={t} className='flex flex-row w-full! gap-5 max-w-[600px] text-xs! sm:text-sm' >
              <div className="text-left! w-[20vw]! text-xs!">{t}:</div> <div className="text-left! w-[80vw]! text-xs!" >{devinfo[t]}</div></div>
           )
          })
        } */}

      </div>
         
    {/* <LoginButton />  */}

       
   {/* <CreateWalletButton /> */}

   {/* <WalletList /> */}
      <div className='' >
           {/* <iframe className='m-0! z-50! bg-amber-300! relative! p-[-25px]! rounded-sm' src="https://trocador.app/anonpay/wvX88X5ZqS" height={295} width={350} scrolling="no"></iframe> */}



{/* <div className='w-[400px] h-[300px] text-sm! mt-5 flex flex-1' >
  <embed src="https://trocador.app/anonpay/BSCUs0dPqT" className='flex flex-1' />
</div> */}


            </div>
 

    </div>

  );
// } 
// else {
//   return (
//     <div>hhhhhhhh</div>
//   )
// }
}






const ddd = 
<div className='dark:fill-white w-[25px]' >
<svg
   version="1.1"
   id="Layer_1"
   x="0px"
   y="0px"
   width="100%"
   viewBox="0 0 1024 1024">
<path
   id="path34798"
   d="m 435.46094,175.67383 c -29.16358,-0.008 -58.32666,0.002 -87.49024,0.008 -9.12725,0.002 -11.14529,1.97475 -11.13476,11.13281 0.018,15.66474 -0.0247,31.33087 0.23437,46.99219 0.0751,4.54318 -1.36032,6.06438 -6.00195,6.00391 -17.99503,-0.23439 -35.99417,-0.12233 -53.99219,-0.0762 -6.00485,0.0155 -9.2832,2.61279 -9.24805,8.06445 0.0837,12.98025 -1.08248,26.04169 0.95899,38.92578 3.44208,21.72327 13.65326,39.42206 32.18359,51.91406 9.387,6.32813 20.0026,8.97122 30.97461,10.32227 3.96756,0.48855 4.89688,2.25461 4.88867,5.82812 -0.0553,23.99713 -0.0648,47.99625 0.13672,71.99219 0.0379,4.51978 -1.30835,6.06625 -5.97656,6 -17.49463,-0.24826 -34.99405,-0.10752 -52.49219,-0.0937 -9.07235,0.007 -10.71869,1.6929 -10.71875,10.84375 -3.9e-4,46.82822 0.001,93.65613 -0.006,140.48437 -10e-4,10.05396 3.01795,13.08729 13.13086,13.09376 16.66486,0.0106 33.32959,0.0486 49.99414,-0.0215 3.63413,-0.0153 6.06897,0.60828 6.04688,5.11523 -0.11026,22.49685 -0.0696,44.995 -0.006,67.49219 0.008,2.89221 -1.17246,4.23004 -4.00195,4.58203 -3.62363,0.45069 -7.27469,0.5932 -10.84961,1.5918 -27.7388,7.74829 -43.62436,26.86871 -51.31055,53.66992 -3.72397,12.98529 -2.76178,26.42188 -2.85352,39.72461 -0.0854,12.38605 2.20698,14.62854 14.4668,14.66602 16.49762,0.0504 32.99494,0.21927 49.49219,0.17969 3.59134,-0.009 5.22687,1.14929 5.01367,4.90039 -0.19824,3.48736 -0.0139,6.99578 0.006,10.99414 0.0143,11.49591 0.0248,22.4931 0.0371,33.49023 0.0106,9.41809 2.85236,12.42932 12.125,12.44727 28.66345,0.0554 57.32678,0.0685 85.99023,0.0254 8.974,-0.0135 11.07718,-2.21216 11.08008,-11.35547 0.004,-13.66504 -0.0678,-27.33124 -0.14258,-40.9961 -0.0517,-9.45214 -0.0771,-9.38794 9.44727,-9.46289 30.81015,-0.24261 61.66272,0.94904 92.40625,-1.82812 31.57434,-2.85217 61.55212,-11.711 89.2832,-26.98828 49.13068,-27.06629 86.44391,-65.96942 111.25391,-116.23242 18.43286,-37.34321 27.89275,-77.18415 28.66016,-118.94532 0.68182,-37.10495 -5.98713,-72.90387 -19.9629,-107.22851 -17.67039,-43.4015 -44.55963,-80.30365 -80.62304,-110.19922 -48.46704,-40.17777 -104.31171,-61.39798 -167.36133,-62.93164 -18.987,-0.46189 -37.99652,-0.21152 -56.99219,-0.01 -4.52383,0.0486 -6.08053,-1.2084 -6.00781,-5.89453 0.24554,-15.82745 0.0978,-31.66279 0.0312,-47.49414 -0.035,-8.34297 -2.44531,-10.7243 -10.66992,-10.72656 z m -56.26367,34.5 c 8.15432,0.3132 16.3359,0.32433 24.49218,0.0566 4.49164,-0.1472 6.14511,1.19687 6.08399,5.91797 -0.22867,17.66134 -0.0778,35.32769 -0.0488,52.99218 0.0106,6.48846 0.3451,6.82148 6.72851,6.82618 32.66258,0.0242 65.3241,0.12961 97.98633,0.0273 28.41822,-0.0886 55.18933,7.49597 80.5,19.2793 72.98163,33.97644 120.08112,89.8825 139.6875,168.41015 5.80323,23.24298 6.08326,46.76764 4.50782,70.46289 -2.64051,39.71546 -14.60798,76.60303 -35.9961,109.90625 -32.50818,50.61817 -77.45154,85.12232 -136.41211,100.01758 -10.18121,2.57209 -20.59039,3.72779 -31.14453,3.71875 -39.99505,-0.0341 -79.99127,0.0585 -119.98633,0.12305 -2.2947,0.004 -4.68463,-0.42517 -6.54101,0.82812 1.35449,16.95429 0.39822,33.72113 0.61328,50.46875 0.14789,11.51947 0.0404,11.52027 -11.58789,11.52735 -6.49921,0.004 -13.00403,-0.13955 -19.4961,0.0801 -3.75329,0.12683 -5.37191,-0.91712 -5.32617,-5.02539 0.19306,-17.32917 -0.17572,-34.66858 0.27539,-51.98829 0.13718,-5.26727 -1.67441,-6.08281 -6.19336,-6.03711 -18.82852,0.19057 -37.66003,0.12497 -56.49023,0.084 -2.25339,-0.005 -4.65298,0.59936 -6.73438,-0.82422 2.04554,-17.71283 14.95554,-37.20044 36.52539,-36.59961 9.14734,0.25482 18.31229,-0.23181 27.4668,-0.125 3.78467,0.0442 5.29764,-1.09442 5.28711,-5.13086 -0.12082,-46.32312 -0.13468,-92.64563 -0.0312,-138.96875 0.009,-4.16736 -1.39978,-5.48718 -5.49414,-5.45703 -18.99628,0.14008 -37.99475,0.0361 -56.99219,0.0215 -7.25879,-0.006 -7.44217,-0.16967 -7.49414,-7.65039 -0.0324,-4.66583 0.20403,-9.34417 -0.0508,-13.99609 -0.2507,-4.58087 1.60794,-6.11999 6.13281,-6.0957 25.49598,0.13678 50.99158,0.0764 76.48828,0.0449 35.8289,-0.0442 71.65757,-0.1004 107.48633,-0.19922 10.32459,-0.0284 20.65393,-0.0903 30.97266,-0.39648 4.5365,-0.13453 6.89593,1.08361 6.59766,6.15429 -0.32227,5.47907 -0.27549,11.00208 0.006,16.48633 0.22394,4.3877 -1.42633,5.74878 -5.78124,5.7168 -22.99595,-0.16882 -45.99497,-0.0716 -68.99219,-0.0625 -13.99832,0.006 -27.99631,0.0692 -41.99414,-0.01 -3.15845,-0.0174 -4.7544,0.50846 -4.73828,4.38281 0.19088,45.82666 0.18618,91.6532 0.23046,137.48047 0.007,7.69324 8.6e-4,7.69208 7.75391,7.68555 45.32694,-0.038 90.65384,-0.0372 135.98047,-0.17187 4.57825,-0.0136 9.87671,1.05908 12.16406,-5.14844 0.37433,-1.01575 2.47229,-1.51294 3.85742,-2.02344 66.78406,-24.61432 107.63428,-73.17664 126.73438,-140.32422 8.7016,-30.591 8.51178,-62.19931 0.90234,-93.47265 -9.23474,-37.95298 -26.97149,-71.32435 -54.50195,-98.98829 -30.48309,-30.6299 -67.0719,-50.10913 -110.19922,-56.11523 -12.20489,-1.69971 -24.60464,-1.17657 -36.93164,-1.00781 -27.82477,0.18976 -54.64951,0.42468 -81.47461,0.5039 -3.63422,0.0108 -4.81424,1.00513 -4.7832,4.87696 0.29379,36.65646 0.33175,73.31518 0.52343,109.97265 0.0169,3.23465 -1.23178,4.46869 -4.41406,4.43164 -9.1644,-0.10684 -18.3324,-0.14763 -27.49609,-0.0254 -3.55145,0.0474 -4.57709,-1.51678 -4.56445,-4.84179 0.10052,-26.4964 0.10372,-52.99357 0.10937,-79.49024 0.002,-10.32541 -0.15441,-20.65249 -0.0527,-30.97656 0.0329,-3.35382 -1.59086,-4.36478 -4.54297,-4.4707 -10.8049,-0.38758 -21.62854,0.42392 -32.4336,-0.72461 -1.398,-0.14861 -2.45831,-0.24424 -3.43554,-0.75 -0.11969,0.11632 -0.32289,0.20407 -0.60938,0.21484 -0.0377,0.001 -0.33767,-0.025 -0.54297,-0.0625 -0.0246,0.0402 -0.0999,0.005 -0.14843,0 -0.19537,-0.0193 -0.34009,-0.0836 -0.50196,-0.18555 -0.0122,-0.01 -0.0246,-0.0198 -0.0371,-0.0293 -0.003,-9.9e-4 -0.003,4e-4 -0.008,-0.002 -0.0626,-0.0283 -0.12485,-0.0559 -0.18555,-0.0879 -0.0342,-0.0179 -0.0648,-0.0421 -0.0976,-0.0625 -0.0292,-0.0199 -0.0461,-0.0287 -0.0625,-0.0371 0.0207,0.006 0.0494,0.012 0.0859,0.0137 0.056,0.003 0.11032,-0.0145 0.16602,-0.0215 4e-4,-10e-4 0.0158,-0.004 0.01,-0.004 -0.42717,-0.0101 -0.45588,0.009 -0.7168,-0.18165 -0.10407,-0.007 -0.197,-0.0546 -0.28516,-0.10742 0.0136,0.008 0.0278,0.0155 0.043,0.0195 0.0372,0.01 0.12408,0.0263 0.15625,0.0274 0,0 0.002,0 0.002,0 0.0121,2.2e-4 0.0161,-0.002 0.002,-0.008 -0.0473,-0.0199 -0.0974,-0.0298 -0.14844,-0.0391 0.0184,0.006 0.013,0.004 0.0352,0.0117 -0.0328,-0.008 -0.0687,-0.0103 -0.10157,-0.0176 0,0 -0.002,-0.002 -0.002,-0.002 -0.017,-0.004 -0.0337,-0.007 -0.0488,-0.0156 -0.004,-0.002 -0.006,-0.006 -0.01,-0.008 -0.015,-0.005 -0.0306,-0.009 -0.0449,-0.0156 -0.006,-0.003 -0.0141,-0.0108 -0.0215,-0.0156 -0.051,-0.0167 -0.0853,-0.0308 -0.20312,-0.0898 -0.031,-0.0155 -0.061,-0.0329 -0.0918,-0.0488 -0.17785,0.0441 0.0476,0.008 -0.32813,-0.20312 -0.0534,-0.03 0.0878,0.0866 0.12305,0.13671 0.007,0.0102 -0.0241,-0.008 -0.0352,-0.0137 -0.14886,-0.0769 -0.15561,-0.0828 -0.28124,-0.1582 -0.17925,0.01 -0.34248,-0.0732 -0.47657,-0.18555 0.0423,0.0332 -0.005,0.009 -0.0645,-0.0254 -0.13212,-0.0484 -0.24732,-0.13323 -0.41016,-0.18554 -0.24507,-0.0674 -0.48032,-0.16552 -0.70312,-0.28711 -0.0429,-0.0104 -0.0657,-0.0208 -0.0137,-0.006 0.004,0.002 0.009,0.003 0.0137,0.006 0.0396,0.01 0.0973,0.02 0.13086,0.008 0.0761,-0.0276 0.14041,-0.0776 0.20703,-0.125 -0.20041,0.0151 -0.40229,0.006 -0.60352,0.008 0.0393,0.0403 0.0375,0.0533 -0.0312,0.0293 -0.0107,-0.004 -0.22016,-0.0798 -0.25586,-0.0996 -0.0527,-0.0291 -0.10164,-0.0651 -0.15234,-0.0977 -0.0598,-0.1064 -0.097,-0.23061 -0.17969,-0.32031 -0.30209,-0.32767 0.11138,0.25377 0.10938,0.25977 -0.005,0.0141 -0.0289,-8.6e-4 -0.043,-0.006 -0.0691,-0.0238 -0.13698,-0.0536 -0.20508,-0.0801 0.11921,0.028 -0.107,-0.0731 -0.23242,-0.13282 -0.0252,-3.8e-4 -0.0511,-9.6e-4 -0.0762,-0.002 -0.004,-0.004 -0.008,-0.008 -0.0117,-0.0117 -0.07,-0.0237 -0.21089,-0.094 -0.23438,-0.10547 -0.0169,-0.009 -0.0345,-0.0173 -0.0508,-0.0273 -0.0259,-0.0155 -0.073,-0.0442 -0.11523,-0.0703 -0.066,-0.0129 -0.13315,-0.0262 -0.19922,-0.0391 -0.0955,-0.0517 -0.1131,-0.0635 -0.1875,-0.0996 -0.0116,-0.006 -0.0476,-0.0196 -0.0352,-0.0156 0.21146,0.0625 0.10519,0.0389 0.44141,-0.0449 0.002,-0.002 0.004,-0.002 0.006,-0.004 -0.14086,-0.0764 -0.27304,-0.18486 -0.41016,-0.27343 -0.18304,0.0251 -0.30903,0.0268 -0.38672,0.0117 0.0442,0.0937 0.12492,0.19913 0.19141,0.22852 0.014,0.006 0.0236,0.008 0.0352,0.0117 0.0827,-0.004 0.16538,-0.0155 0.24804,-0.0195 -0.12923,0.0238 -0.16191,0.0491 -0.24804,0.0195 -0.0407,0.002 -0.0825,0.004 -0.12305,0 -0.002,-1.9e-4 -0.004,-0.002 -0.006,-0.002 -0.0314,-0.005 -0.0597,-0.0207 -0.0879,-0.0371 -0.0509,-0.0232 -0.093,-0.0443 -0.0469,-0.0254 0.0163,0.007 0.0314,0.0163 0.0469,0.0254 0.0341,0.0155 0.0734,0.0326 0.0879,0.0371 0.0121,0.004 0.008,-7.1e-4 -0.0254,-0.0195 -0.0651,-0.0369 -0.0999,-0.0528 -0.13281,-0.0684 -0.12978,-0.0341 -0.27794,-0.0846 -0.23047,-0.11915 -0.033,-0.0253 -0.0671,-0.0528 -0.0859,-0.0664 -0.19806,-0.0914 -0.35629,-0.25225 -0.55273,-0.34375 -0.14537,-0.11164 -0.25559,-0.19547 -0.38477,-0.31836 -0.018,-0.002 -0.0351,-0.005 -0.0527,-0.008 -0.1099,-0.0203 -0.0577,-0.0927 -0.0957,-0.0742 -0.0826,-0.0577 -0.0854,-0.0587 -0.0859,-0.0605 0.002,0.002 -0.005,-0.003 -0.008,-0.004 -0.0334,-0.015 -0.0663,-0.0316 -0.0996,-0.0469 -0.34278,-0.25052 -0.0539,-0.0228 -0.2539,-0.21094 -0.016,-0.0152 0.0328,0.0303 0.0449,0.0488 0.006,0.009 -0.019,-0.007 -0.0293,-0.01 -0.12144,-0.0703 -0.12739,-0.072 -0.13672,-0.0781 -0.18481,-0.0202 -0.3404,-0.0998 -0.46289,-0.22852 -0.003,5.2e-4 -0.0125,-0.002 -0.0195,-0.004 -0.0271,0.0478 -0.0435,0.0983 -0.11133,0.13476 -10.58148,-6.10281 -15.24423,-16.15173 -17.93164,-27.46875 -0.57046,-2.40234 0.57059,-3.90383 3.10547,-4.01757 4.9787,-0.22364 9.96002,-0.49985 14.94141,-0.51758 15.16458,-0.054 30.33314,-0.17667 45.49219,0.12695 4.57436,0.0916 5.59844,-1.48294 5.55273,-5.72266 -0.19232,-17.82899 0.0357,-35.66114 -0.15234,-53.49023 -0.0471,-4.46631 1.22393,-6.32558 5.9375,-6.14453 z m -56.81446,97.10351 c 0.005,-8e-4 -0.002,-0.007 -0.0117,-0.0156 3.2e-4,3.8e-4 -3.1e-4,0.002 0,0.002 0.004,0.005 0.008,0.009 0.0117,0.0137 z m 1.17969,0.67188 c 0.0491,0.0351 0.0931,0.089 0.15234,0.0937 0.13284,0.0113 0.51589,0.005 0.39649,-0.0547 -0.16413,-0.0815 -0.36492,-0.0226 -0.54883,-0.0391 z m 1.02344,0.72851 c 0.0458,0.0352 0.0915,0.0676 0.11328,0.0762 0.0263,0.0104 0.0543,0.0193 0.082,0.0254 -0.0967,-0.0424 -0.0411,0.004 -0.1582,-0.11719 -0.0185,0.004 -0.0296,0.0102 -0.0371,0.0156 z m 0.23047,0.11915 c 0.10529,0.0276 0.19889,0.0445 0.15039,0.0254 -0.0587,-0.0231 -0.12174,-0.0296 -0.1836,-0.043 0.007,0.003 0.0249,0.0137 0.0332,0.0176 z m 5.11328,2.17968 c 0.0136,0.005 0.027,0.0102 0.041,0.0137 0.0281,0.007 0.0572,0.0124 0.0859,0.0176 -0.0763,-0.0251 -0.1139,-0.0367 -0.14648,-0.0469 0.006,0.005 0.0126,0.0111 0.0195,0.0156 z m 0.27343,0.0781 0.0371,0.0332 c 0.003,4e-4 0.007,-2.9e-4 0.01,0 -0.0174,-0.0129 -0.0273,-0.0185 -0.0469,-0.0332 z m -5.75195,-6.06055 c 0,0.005 3e-5,0.009 0,0.0137 0.003,0.004 0.005,0.008 0.008,0.0117 0.002,-0.006 0.004,-0.0117 0.006,-0.0176 -0.004,-0.003 -0.009,-0.005 -0.0137,-0.008 z m -2.0039,2.17383 c -0.012,0.0139 -0.024,0.0283 -0.0332,0.043 0.0741,0.0543 0.14837,0.10612 0.23633,0.12695 0.0497,0.0118 0.14909,-0.0104 0.21484,-0.0352 -0.10443,-0.0354 -0.21413,-0.0311 -0.32226,-0.084 -0.0247,-0.0121 -0.0462,-0.03 -0.0684,-0.0469 -0.01,-0.001 -0.0181,-0.003 -0.0273,-0.004 z m 0.25976,0.21289 c 0.008,0.0156 0.0485,0.068 0.0723,0.0781 0.015,0.006 0.0128,0.005 0.0234,0.01 -0.0123,-0.0148 -0.0385,-0.04 -0.0918,-0.0879 -0.006,-0.006 -0.007,-0.005 -0.004,0 z m 3.04297,1.65625 c -0.0178,0.009 0.13943,0.17313 0.20312,0.22851 0.0147,0.0127 0.0447,0.0179 0.0723,0.0215 -0.081,-0.0875 -0.15288,-0.186 -0.25586,-0.24414 -0.0105,-0.006 -0.017,-0.007 -0.0195,-0.006 z m -0.0859,0.0762 c 0.002,0.001 0.004,0.003 0.006,0.004 0.0195,0.009 0.0855,0.0138 0.0645,0.01 -0.0233,-0.005 -0.047,-0.009 -0.0703,-0.0137 z m 1.38477,0.0625 c -0.006,0.0111 -0.01,0.0202 -0.002,0.0156 0.005,-0.003 0.009,-0.007 0.0137,-0.01 -0.005,-0.003 -0.007,-0.003 -0.0117,-0.006 z m -0.89258,0.15234 c 0.009,0.005 0.0187,0.0119 0.0293,0.0137 0.0595,0.01 0.24144,0.005 0.18164,-0.002 -0.0697,-0.009 -0.1406,-0.0107 -0.21094,-0.0117 z m 2.46484,1.0586 c 0.009,0.008 0.0198,0.008 0.0527,0.004 -0.018,-9.4e-4 -0.0358,-0.001 -0.0527,-0.004 z m 1.35157,0.3457 c -0.18297,0.0276 -0.28875,0.0481 -0.35938,0.0645 0.081,0.0215 0.0985,0.0326 0.1211,0.0293 -1.2e-4,-0.003 0.003,-0.004 0.01,-0.002 0.0267,-0.007 0.0669,-0.0306 0.22852,-0.0918 z m 2.0039,0.48242 c -0.0504,0.16048 -0.10456,0.31913 -0.17968,0.46875 0.06,0.0152 0.10676,0.0222 0.11132,-0.002 0.0293,-0.1545 0.0524,-0.31006 0.0684,-0.4668 z m 157.66797,36.99414 c 12.32963,-0.079 24.65141,0.0778 36.94727,1.21485 14.56414,1.34683 28.25421,6.52618 41.24414,13.01953 45.8941,22.94137 77.27929,58.5607 90.9414,108.3125 17.71393,64.50708 -6.38678,134.46728 -59.03515,173.81445 -18.38306,13.73871 -38.42841,23.90674 -61.05078,28.49414 -4.87262,0.9881 -9.82319,1.66309 -14.84766,1.6543 -23.66428,-0.0414 -47.32977,-0.007 -70.99414,-0.0215 -6.55301,-0.004 -6.64505,-0.0959 -6.65039,-6.79102 -0.0161,-20.33136 -0.0133,-40.66083 0.008,-60.99219 0.009,-9.71734 0.0369,-9.79034 9.60742,-9.79297 32.99668,-0.009 65.99359,0.0319 98.99024,0.0586 10.56061,0.009 13.48376,-2.83301 13.48047,-13.19336 -0.0147,-45.82886 -0.0353,-91.6594 -0.0606,-137.48828 -9.2e-4,-1.66571 0.0415,-3.34128 -0.12305,-4.99414 -0.65844,-6.6149 -2.9804,-8.77048 -9.60547,-8.79883 -10.99835,-0.0471 -21.99756,-0.0123 -32.99609,-0.0117 -24.83102,7e-4 -48.66116,0.005 -72.49219,0 -6.74209,-10e-4 -6.74957,-0.0138 -6.75781,-6.47656 -0.0301,-23.66431 0.0797,-47.32874 -0.19141,-70.99024 -0.0584,-5.09915 1.8234,-6.89886 6.59571,-6.82226 12.32428,0.19781 24.6606,-0.11631 36.99023,-0.19532 z m 36.77149,120.30274 c 3.01049,-0.0307 4.56671,1.45038 4.52929,4.62109 -0.0765,6.49536 -0.0725,12.99277 -0.004,19.48828 0.0315,2.94153 -1.20349,4.24167 -4.18946,4.16797 -4.66223,-0.11514 -9.32928,-0.0531 -13.99414,-0.0527 -67.14187,0.005 -134.2839,0.0127 -201.42578,0.0195 -7.98135,7.9e-4 -7.98349,-5.5e-4 -7.98633,-7.87891 -0.002,-4.49829 0.23996,-9.01291 -0.0664,-13.49023 -0.32355,-4.72843 1.42496,-6.56967 6.23632,-6.48828 12.3252,0.20852 24.65567,0.0731 36.98438,0.0742 56.47928,-0.0268 111.95822,-0.0525 167.4375,-0.10938 4.15955,-0.004 8.31818,-0.30917 12.47852,-0.35156 z" />



</svg>
</div>

