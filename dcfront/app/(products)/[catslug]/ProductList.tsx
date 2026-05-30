//@ts-nocheck
"use client"
import wk from '@/lib/wk';
import { cn } from '@/lib/utils'
import Link, { useLinkStatus } from 'next/link';
import { useParams, useRouter, useSearchParams, usePathname } from 'next/navigation';
import { useEffect, useCallback } from 'react';
import { delay } from '@/lib/utils';
import { defStore, simpleStore } from '@/store/zustand_1';
// import Loader from '@/components/Loader';
import Loading from './loading'
import { Skeleton } from '@/components/ui/skeleton'
import { useState } from 'react';
import { Button } from "@/components/ui/button"
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import fetchClient from '@/app/actions/fetchClient';

// import { getBrand } from '@/app/actions/dal';
// import { apiClientFetch } from '@/app/lib/api-client'

export function regionCalc(item, store, cart) {
    'use client'
    const iregions = item.regions.length > 0 ? item.regions.map((f) => f.toLowerCase()) : item.regions = ['ww']
    // console.log(findFirstTwoMatches(store.dget(["region"]), iregions))
    const bas = cart?.products?.filter((f) => f.brand?.slug === item?.slug)[0]
    if (bas) {
      return bas.region
      // store.set({ region: [...new Set([bas.region, ...store.dget(["region"])])] })
    } else if (findFirstTwoMatches(store.dget(["region"]), iregions)?.length > 0) {
      return findFirstTwoMatches(store.dget(["region"]), iregions)[0]?.toLowerCase()
      // item.regions && store.set({ region: [...new Set([item.regions[0], ...store.dget(["region"])])] })
    } else if (findFirstTwoMatches(store.dget(["region"]), iregions) && (findFirstTwoMatches(store.dget(["region"]), iregions)[0] !== (store.dget(["region"]) && store.dget(["region"])[0]))) {
      return (findFirstTwoMatches(store.dget(["region"]), iregions)[0]?.toLowerCase() ?? iregions[0]?.toLowerCase())
      // store.set({ region: [...new Set([findFirstTwoMatches(store.dget(["region"]), item.regions)[0], ...store.dget(["region"])])] })
    }
  }




// function getCookie(name=null) {
//   if (typeof document === 'undefined') return null;
//   if(!name) return document.cookie;
//     return document.cookie.split('; ').find(row => row.startsWith(name + '='))?.split('=')[1]
// }

function classNames(...classes: any[]) {
  return classes.filter(Boolean).join(' ')
}

const findFirstTwoMatches = (arr1, arr2) =>
  arr1?.filter((value) => new Set(arr2).has(value)).slice(0, 2);


export default function ProductsList({}) {
  'use client'
  const store = defStore()
  const simste = simpleStore()
  const cart = simste.pget(["cart"])
  const router = useRouter();
  const params = useParams();
  const [data, setData] = useState()

// wk.useClientLoadDebug("ProductList")
  
  const [IsClient, setIsClient] = useState(false)

  useEffect(() => {
   setIsClient(true)
}, [])



  useEffect(()=>{
    const id = setTimeout(async () => {
      if(params.catslug){
        simste.pset(['brandloader'], true)
        const Data = await fetchClient('GET', "brand", {category__slug: params.catslug}, null)
        
          if(Data?.detail === "Invalid token Error: HTTP 401") window.location.reload()
        // const Data = await getBrand({ filter: params.catslug })
        Data && simste.pset(["prodlist"], Data.data)
        setData(Data.data)
        store.dset(["productlist"], Data.data); 
        simste.pset(['brandloader'], false)
      }
      }, 0)

    return () => {
      clearTimeout(id)
    }
  },[])
    
      // ###############################
      useEffect(() => {
        const id = setTimeout(() => {
 
        }, 0)
        return () => {clearTimeout(id)} 
      }, [])
      // ###############################


  
  function handleClick(e) {
    e.preventDefault()
    e.stopPropagation()
    const item = brands?.filter((f) => f.slug === e.target.id)[0]
    regionCalc(item, store, cart)
  }
 
  
  // if(!cart?.currency?.shortname) return <Loading />
  if(!IsClient || simste.pget(['brandloader'])) return <Loading />
  return (
    <div className="mx-auto max-w-7xl text-center">
      <div className="mx-0 flex flex-wrap gap-2 justify-around"
        onClick={(e) => {
          // if(e.target.localName === 'div' && e.target.className.includes('k-overlay')) ss()
        }}
      >
        {
           (data && data?.length > 0) && data?.map((item) => {
            return (
              // <ProdItem key={item.slug} {...{regionCalc, item, params, router}} />
              <ItemCard key={item.id} {...{regionCalc, item, params, router, simste, store, cart}} />
              )
          })
        }
      </div>
    </div>
  )
}



function ItemCard({regionCalc, item, params, router, simste, store, cart}){
  'use client'
  const searchParams = useSearchParams()
  const pathname = usePathname()
  const region = regionCalc(item, store, cart)
  if(!region) return

  useEffect(()=>{simste.pset(["regionCalc"], region)},[])

  const createQueryString = useCallback(
    (obj) => {
      const param = new URLSearchParams(searchParams.toString())
       Object.keys(obj).forEach((k,v)=>param.set(k, obj[k]))
      return param.toString()
    },
    [searchParams]
  )





  // console.log(Object.keys(obj).map((m)=>mobj[m]))
  
const [imageSrc, setImageSrc] = useState(item.image || "/media/no-image.png");
  
  return (
    <Card className='p-[2px] sm:w-[135] sm:h-[135] w-[120] h-[120] flex justify-center items-center shadow-inner shadow-neutral-300 border border-neutral-500' >
       {/* <Button onClick={(e)=>rrr()} >fffffff</Button> */}
      <div 
                className="flex justify-center items-center relative"
              >
                
                <Link 
                  href={{ pathname: `/${params.catslug}/${item.slug}`, query: { r: region } }}
                  params={{reg:region}}
                  prefetch={false}
                  className={cn(!item.in_stock && 'opacity-60')}
                  onPointerEnter={(e)=>{
                    // console.log(e)
                    if(e.pointerType === "touch"){
                      e.target.classList.remove("hover:scale-[1.10]")
                      // e.target.classList.add("active:scale-[0.9]")
                    }
                  }}
                  >
                {/* <Skeleton className="rounded-xs absolute top-2 left-2 right-2 bottom-2" /> */}
                  <img
                    alt={item.title}
                    onError={() => {
                        setImageSrc("/media/no-image.png");
                      }}
                    src={imageSrc}
                    width={138}
                    height={138}
                    className="flex flex-1 aspect-1 rounded-[8px] box-border overflow-hidden border border-neutral-500 active:scale-[0.95] sm:w-[125px] sm:h-[125px] w-[110px] h-[110px]"
                  />
                </Link>
                {/* <img
                    alt={'outofstock'}
                    src={'/media/def/outofstock2.svg'}
                    className="flex flex-1 aspect-1 absolute top-0 bg-background"
                  /> */}
                  {!item.in_stock && 
                  <div className="flex! justify-center! items-center! px-2 py-[0.2rem] absolute top-[0.10rem] bg-background rounded-md text-red-500 font-bold!">
                    OUT OF STOCK
                  </div>}
            </div>
      {/* </CardContent> */}
      {/* <CardFooter>
        <p>Card Footer</p>
      </CardFooter> */}
    </Card>
  )
}
