"use client";
export const dynamic = "force-dynamic";
import { useMemo, createRef } from "react";
// import useAxiosFunction from "@/hooks/useAxiosFunction";
// import { defStore, simpleStore, perStore } from "@/store/zustand_1";
// import useWindowSize from "@/hooks/UseWindowSize";
import { delay } from "@/lib/utils";
// import useDetectTouch from "@/hooks/useDetectTouch";
import { signal, Signal } from "@preact/signals-react";
import { encryptWithPublicKey } from "./libsodium_crypto";
import Loader from "@/components/Loader";
import { generatePassword } from '@/lib/utils'
import { dateFormat } from "@/lib/utils";
import { sobj } from "@/store/signamanager/signalFnProd";
import { LoaderPinwheel} from 'lucide-react';
import { useClientLoadDebug } from "./DebugInstrumenty";



import { RedirectType } from "next/navigation";
import { Button } from "@/components/ui/button";


const refsObj = {}
const signalObj = {}

  

  export function refProxy(target=refsObj){
    "use client";
    return new Proxy(target, {
      set: (obj, prop, value) => {
        obj[prop] = createRef(0)
      // console.log(obj[prop]);
        return true;
      },
      get: (obj, prop) => {
        if(!obj[prop]?.current) obj[prop] = createRef(0)
        // console.log(prop);
      //   console.log(obj);
        return obj[prop]
      } 
    })
  }


  const withDefaultValue = (target=signalObj,k) => {
    
    const ob = new Proxy(target, {
      set: (obj, prop, value) => {
        // console.log(obj)
        if (prop in obj && obj[prop] instanceof Signal) { obj[prop].value = value} 
        else {
          obj[prop] = signal(value)
          obj[prop].subscribe((v) => {
            if(!obj[prop].gg) obj[prop].gg = v
            // if(obj[prop].gg !== v){
            //   console.log('subsc',obj)
            //   obj[prop].gg = v
            // }
            if(prop === 'paypopover'){
              if(obj['basketsignal']) obj['basketsignal'].value = `${v}`
            }
            // console.log('subsc',obj)
          obj[prop].gg = v
          });
        }
        return true;
      },
      get: (obj, prop) => {
        // console.log('get', prop)
        
        return obj[prop]
      }
    })
    return ob
  }

  // const gg = withDefaultValue()




  const pObj = {}

function simProxy(target=pObj, simste){
    "use client";
    return new Proxy(target, {
      set: (obj, prop, value) => {
        // console.log(obj[prop]);
        // console.log(value);
        if(obj[prop] !== value){
            obj[prop] = value
            simste.pset([prop], value)
        } 
        // obj[prop] = createRef(0)
        return true;
      },
      get: (obj, prop) => {
        // console.log(prop);
      //   console.log(obj);
        return simste.pget([prop])
      } 
    })
  }

    const storeObj = {}

function storeProxy(target=storeObj, store){
    "use client";
    return new Proxy(target, {
      set: (obj, prop, value) => {
        // console.log(obj[prop]);
        // console.log(value);
        if(obj[prop] !== value){
            obj[prop] = value
            store.dset([prop], value)
        } 
        // obj[prop] = createRef(0)
        return true;
      },
      get: (obj, prop) => {
        // console.log(prop);
      //   console.log(obj);
        return store.dget([prop])
      } 
    })
  }

      const usestateObj = {}

function useStateProxy(target=usestateObj, useStateSet){
    "use client";
    return new Proxy(target, {
      set: (obj, prop, value) => {
        // console.log(obj[prop]);
        // console.log(value);
        if(obj[prop] !== value){
            obj[prop] = value
            useStateSet({prop:value})
        } 
        // obj[prop] = createRef(0)
        return true;
      },
      get: (obj, prop) => {
        // console.log(prop);
      //   console.log(obj);
        return obj[prop]
      } 
    })
  }







function prxy(obj, callback) {
  return new Proxy(obj, {
    set(target, property, value) {
      target[property] = value;
      callback(property, value);
      return true;
    }
  })
}




function debounc(func, delay) {
  "use client";
  let timeout;
  return (...args) => {
      clearTimeout(timeout);
      timeout = setTimeout(() => func(...args), delay);
  };
}

          
const wk = {
    // axfn: useAxiosFunction,
    genpass: generatePassword,
    simProxy: simProxy,
    storeProxy: storeProxy,
    // useStateProxy: useStateProxy,
    delay: delay,
    // detectTouch: useDetectTouch,
    encryptWithPublicKey:encryptWithPublicKey,
    cryptkey: "LoAUDhhUnrJ7DimoCE5FUi5LZa9MqLmbd/Ur7pF5jC4=",
    classes: {
        flex_col_2center: 'flex flex-col justify-center items-center',
        bglight: "bg-gradient-to-br from-[#a1ffce] to-[#faffd1] flex justify-center items-center m-0 font-sans text-[#333]"
    },
    signal: signal,
    useClientLoadDebug: useClientLoadDebug,
    dateFormat: dateFormat,
        sobj:sobj,
    debounc:debounc,
    GetProduct(){
        const [response, loading,  error, axiosGet] = useAxiosFunction('GetProduct')
        return {response, loading,  error, axiosGet}
    },
    refs:refProxy(),
    signalP:withDefaultValue(),
    Loader:Loader,
    prxy:prxy
}

export default wk




const FetchOb = {
    
}
