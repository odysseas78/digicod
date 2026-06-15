"use client";
import dynamic from 'next/dynamic';
import { Suspense } from 'react';
import wk from '@/lib/wk';
import { signal } from '@preact/signals-react';
import { Mail, PowerOff, PlusCircle } from 'lucide-react';
import { useParams, useRouter, usePathname, useSearchParams } from "next/navigation";
import { useEffect, useRef, useState, useTransition } from 'react';
import PriceLabelDB from './ProductView/PriceLabelDB';
import SelectRegion from './ProductView/SelectRegion';
import { Button } from "@/components/ui/button"
import Cart from '@/app/checkout/cart/cart';
import useWindowSize from '@/hooks/UseWindowSize';
import AccordionPr from './ProductView/Accordionn';
// import Cookies from 'js-cookie';
// import { cn } from '@/lib/utils';
import fetchActionClient from '@/app/actions/fetchActionBrowser';
import { simpleStore, defStore } from '@/store/zustand_1';
import {
  Popover,
  PopoverTrigger,
  PopoverContent,
} from '@/components/animate-ui/components/radix/popover';
import { getBasket } from '@/app/checkout/cart/cart'
import Loading from './loading'
import useContexData from '@/store/DefContext';




// function getCookie(name=null) {
//   if (typeof document === 'undefined') return null;
//   if(!name) return document.cookie;
//     return document.cookie.split('; ').find(row => row.startsWith(name + '='))?.split('=')[1]
// }
// #############################

// async function setCookie(cname, cvalue, exdays) {
//   const d = new Date();
//   d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
//   let expires = "expires=" + d.toUTCString();
//   document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
// }
// const setCookies = async () => {
//   // const hh = await fpsha256()
//   Cookies.set('_polz', hh, { expires: 7, path: '/' });
//   // alert('Cookie gesetzt!');
// };


const refo = wk.refs
const $s = wk.signalP
const datastate = signal()
const noproducterror = signal(false)
$s.stopnavi = false

function classNames(...classes) {
  return classes.filter(Boolean).join(' ')
}

// um productprice änderung zu prüffen
!$s.zzz && ($s.zzz = 0)


export default function ProductPage({  }) {
  "use client"
  // localStorage.setItem('productData', JSON.stringify(product))
  // console.log('product page')
  const [loading, setLoading] = useState(false)
  const params = useParams();
  const sparams = useSearchParams()
  const pathname = usePathname()
  const store = defStore()
  const region = store.dget(['region'])
  const simste = simpleStore()
  const cart = simste.pget(["cart"])
  const router = useRouter()
  // const product = simste.pget(['product'])
  const [product, setProduct] = useState()
  const productloader = simste.pget(["productloader"])
  const [IsClient, setIsClient] = useState(false)

  // console.log(simste.pget(["reg"]));
  // // console.log(params);
  // console.log("YYY", sparams.get('r'));
  // console.log("region", region[0]);

  useEffect(() => {
   setIsClient(true)
   const id = setTimeout(async () => {
      if(params.brandslug && sparams.get('r')){
        simste.pset(["productloader"], true)
        setLoading(true)
        const Data = await fetchActionClient('GetProduct', { filter: params.brandslug, region: sparams.get('r') })
        if(Data?.detail === "Invalid token Error: HTTP 401") window.location.reload()
        setProduct(Data)
        console.log(Data)
        Data && simste.pset(["product"], Data) 
        setLoading(false)
        setTimeout(()=>{simste.pset(["productloader"], false)},500)
      }
      }, 0)

    return () => {
      clearTimeout(id)
    }
}, [])



  useEffect(()=>{
    const id = setTimeout(async () => {
      if(params.brandslug && sparams.get('r')){
        simste.pset(["productloader"], true)
        const Data = await fetchActionClient('GetProduct', { filter: params.brandslug, region: sparams.get('r') })
        if(Data?.detail === "Invalid token Error: HTTP 401") window.location.reload()
        setProduct(Data)
        Data && simste.pset(["product"], Data) 
        setTimeout(()=>{simste.pset(["productloader"], false)},500)
      }
      }, 0)

    return () => {
      clearTimeout(id)
    }
  },[sparams.get('r')])      
  

  // ###############################
      useEffect(() => {
        const id = setTimeout(() => {
          // !getCookie('_polz') && window.location.reload()
        }, 0)
        return () => {clearTimeout(id)} 
      }, [])
      // ###############################
      // if(!prodData) window.location.reload()
  const [selected, setSelected] = useState();
  const { width } = useWindowSize()

  function fn1(dataattr) {
    if (itemsref.current?.children && itemsref.current?.children?.length > 0) {
      const el = itemsref.current.querySelectorAll(dataattr)
      const el2 = [...el]
      const childrn2 = [...el]
      // childrn2.reverse()
      const allvalues2 = childrn2.map((c) => c.offsetWidth)
      const res = Math.max(...allvalues2)
      // const childrn = [...itemsref.current.children]
      el2.map((c) => c.style.width = res + 'px')
      return res
    }
  }

// ############# Fetch Product #####################
 const curCurrent = useRef()
  useEffect(() => {
    const id = setTimeout(async () => {
      const condition = (curCurrent.current && (curCurrent.current !== cart.currency.shortname))
      if(condition){
        simste.pset(["productloader"], true)
        const Data = await fetchActionClient('GetProduct', { filter: params.brandslug, region: sparams.get('r') })
        if(Data?.detail === "Invalid token Error: HTTP 401") window.location.reload()
        setProduct(Data)
        console.log('GetProduct----')
        Data && simste.pset(["product"], Data) 
        setTimeout(()=>{simste.pset(["productloader"], false)},300)
      }
      }, 0)

    return () => {
      curCurrent.current = cart.currency?.shortname
      clearTimeout(id)
    }
    
  }, [cart.currency?.shortname])
// ###################################

// const mounted = useMounted()

  useEffect(() => {
    const ff1 = () =>{
      fn1('[data-ff]')
      fn1('[data-ss]')
      fn1('[data-bdg]')
    }
    const tid = setTimeout(()=>{
      ff1()
    },30)
    
    return () => {
      clearTimeout(tid)
    }
  }, [width, product, productloader, cart?.currency])

  const itemsref = useRef(null)
  const currency = cart?.currency

  // const [response, loading,  error, axiosGet] = useAxiosFunction('GetProduct')
  // useEffect(()=>{store.set((prev)=>{return {...prev['GetProduct'], ['GetProduct']:response}})},[response])
  // ##################################################
  const prod = product ? product[0] : null

  // const regs = (prod?.brand?.regions && prod?.brand?.regions.length > 0) ? prod?.brand?.regions : ['ww']
  const regions = prod?.brand?.regions.map((f) => {
    let a = f.toLowerCase()
    if (a === 'vd') a = 'vn'
    return a
  })
  setTimeout(() => {
  
  }, 300);
  
  

  
  // useEffect(()=>{ 
  //   const tid = setTimeout(()=>{
      
  //     if((product) && (params?.region !==  product[0]?.region)){
  //       // console.log(params.region)
  //       // console.log(product[0].region)
  //       simste.pget(["product"]) && router.push(`/${simste.pget(["product"])[0]?.region}/${params.catslug}/${params.brandslug}`)
  //     }
  //   },100)

  //   return ()=>{
  //     clearTimeout(tid)
  //   }
    
  // },[product])
    
    
  $s.region.value = region && region[0]

  useEffect(() => {
    wk.debounc(
      product?.length > 0 && product?.forEach(el => {
        el.slug === params.prodslug && setSelected(el)
      }),
      100
    )
  }, [product, params.prodslug, params.catslug, params.brandslug])

  
  
  let prp = {
    selected:selected,
    setSelected:setSelected,
    cart:cart,
    product
  }


  
  // if(!cart.currency?.shortname) return 
  if(!IsClient || loading) return <Loading />
  if(product?.error === "No products found") return <div className='absolute top-0 left-0 right-0 bottom-0 flex justify-center items-center' >
                                                            <img src="/media/def/outofstock2.svg" width={220} className="" /></div>
   return (
    
    product && product.length > 0 ?
    
    <>
    <div ref={itemsref} className='w-full px-px h-full overflow-y-auto' >
      {/* {
        (!cart.currency?.shortname) &&
        <Loading />
      } */}
{/* <Button onClick={() => {po.pr_price = po.pr_price + 1}} >lkölköl</Button> */}
        <div className='flex flex-row justify-between items-start w-full' >
          <div className={'flex flex-col flex-wrap justify-center w-full p-px gap-2'}>
            {selected?.title ?? simste.pget(["product"])[0]?.brand?.title}
            <div className='flex flex-row gap-5 relative'>
              <div>
                <img src={selected?.image || (product && product[0]?.brand?.image) || '/media/no-image.png'} alt='image' className='w-[100px] h-[100px] md:w-[125px] md:h-[125px] aspect-1 rounded-md border-[0.5px] border-neutral-500' />
              </div>
              <div className='flex flex-col gap-[0.30rem] sm:gap-[0.65rem] items-start' >
                <div className='mt[-18px] notranslate'>
                  <SelectRegion regions={regions} />
                </div>
                <div className='flex flex-row gap-1 items-center'>
                  <Mail className='text-green-600' size={20} /> <div className='text-[13px]'>Instant delivery</div>
                </div>
                {/* ####### dcoin cashback ########### */}
                  {/* <div className='flex flex-row items-center gap-[7px]' >
                    <img src={'/media/payment/dccoin.webp'} className='w-[22px] sm:w-[22px] rounded-md' />
                    <span className='text-[0.79rem] italic text-green-500' >+{selected?.dcoinprice || product[0]?.dcoinprice} dcoins</span>
                  </div> */}
                {/* ####### dcoin cashback ########### */}
              </div>
               {(!product[0]?.in_stock) && <img
                    alt={'outofstock'}
                    src={'/media/def/outofstock2.svg'}
                    className="flex! flex-1! w-20! max-w-50! bg-background m-auto"
                  />}
            </div>
            {width < 800 && 
            <div className="flex flex-row flex-wrap justify-center gap-4 w-full mt-4">
              {
                product.map((p) => {
                  prp.p = p
                  // const dcoinprice = p.price / cart.currency.price * 13
                  return (
                  <div key={p.slug} className='flex flex-row gap-[7px] items-center' >
                     <PriceLabelDB key={p.slug} {...prp} getBasket={getBasket} />
                  </div>
                )  
                })
              }
            </div>}
            {cart?.total_products > 0 && 
            <div className='mt-4 w-full'>
              {/* <Suspense fallback={null}> */}
              <Cart checkoutbutton={true} />
              {/* </Suspense> */}
              {/* <MinBasket store={store} currency={currency} simste={simste} /> */}
            </div>}
          </div>
          {width > 800 && 
          <div className="flex flex-row flex-wrap self-start justify-center items-start mt-4 gap-4 w-full relative">
            {
              product.map((p) => {
                prp.p = p
                // const dcoinprice = (p.price / cart.currency.price * 13).toFixed(0)
                return (
                  <div key={p.slug} className='flex flex-row gap-[7px] items-center notranslate' >
                     <PriceLabelDB {...prp} getBasket={getBasket} />
                  </div>
                ) 
              })
            }
          </div>}
        </div>
        <div className='mt-[20px] transition-all duration-500'>
          <AccordionPr {...{ title: (product[0].brand?.title), params: params, store: store, product, regions, selected, currency }} />
        </div>
    </div>
    </>
    
    :
    product && (product.length === 0) &&
    <NoProducts />
  )
}


function NoProducts(){
  const router = useRouter()
  useEffect(()=>{
    const tid = setTimeout(()=>{
      router.replace('/')
      // console.log('no products')
    },1500)
  },[])

  return (
      <div className='absolute top-0 left-0 bottom-0 right-0 flex flex-row justify-center items-center text-lg'>
          No products
      </div>
  )
}
