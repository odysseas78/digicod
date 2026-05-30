'use client';
export const dynamic = "force-dynamic";
import { AvatarIcon, MoonIcon } from '@radix-ui/react-icons';
import React, { useEffect, useState } from 'react';
// import Login from '../../components/Auth/LoginRegister/LoginRegister'
// import LoginModal from '../../components/Auth/LoginRegister/LoginModal';
// import TodoList from '../MyAccount/Table/TableCls'
import useWindowSize from "@/hooks/UseWindowSize";
import useAxiosFunction from '@/hooks/useAxiosFunction';
import wk from '@/lib/wk';
import { useParams, useSearchParams, useRouter } from "next/navigation";
import { Button } from '@/components/ui/button';
// import { createPortal } from 'react-dom';
// import { AlertDialog } from '../../components/Dialogs/DialogCls';
// import { Panel, PanelGroup, PanelResizeHandle } from "react-resizable-panels";
// import { useSyncExternalStore } from 'react';
import { create } from 'zustand'
// import axios from 'axios';
// import { useActionState } from 'react'

async function getFetch(key, params) {
    const prms = {u: key,p: JSON.stringify(params)}
    const urlParams = new URLSearchParams(prms);
  // console.log(urlParams);
  // console.log(host);
  const res = await fetch(`/c/?${urlParams}`, {
    cache: "no-store", // keine Revalidierung/Zwischenspeicherung
  });
  if (!res.ok) throw new Error(`Upstream ${res.status}`);
  const data = await res.json()
  // console.log(data);
  
  return data;
}









class Ssr{

  constructor(){
    this.ddd = false
    this.bc = {
      onClick:(e)=>{
          // console.log(this)
          if(this.ddd){
            this.ddd = false
            return
          }
        if(e.type === 'click'){
          // console.log(e)  
        }
      },
      onMouseDown:null,
      onMouseUp:null,
      onTouchStart:(e)=>{
        this.ddd = true
        if(e.type === 'touchstart'){
          // console.log(this.ddd)  
        }
      },
      onTouchEnd:null,
      // setall(fn){
      //   this.onClick = fn
      //   this.onTouchStart = fn
      //   // return 'n'
      // },
      // getall(){
      //   return this.onClick
      // }
    }
  }

  USer(){
    const [user, setUser] = useState(null)
    return {user, setUser}
  }

}


function classNames(...classes) {
  return classes.filter(Boolean).join(' ')
}

const $s = wk.signalP




const useStore = create((set) => ({
  storSet: (data) => set((state) => {
      return({...state,...data})}),
}))




export default function Homepage({}) {
  // const [aa, bb] = useState(false)
  const store = wk.defSte()
  const simste = wk.simSte()
  // const modal = simplestore
  // const [modals, setModals] = useState([])
  // const [a, setA] = useState(false)
  // const params = useParams()
  // const user = store.user
  // const router = useRouter()



      // ###############################
      useEffect(() => {
        const id = setTimeout(() => {}, 0)
        return () => {clearTimeout(id)} 
      }, [])
      // ###############################


  const searchparams = useSearchParams()





// useEffect(()=>{
//   // redirect wegen fehlende cookies im product page

//   if(decodeURIComponent(searchparams.get('rdr'))?.length > 10){
//     const a = decodeURIComponent(searchparams.get('rdr')).split("/")
    
//     const b = a.filter((f,i)=>  i >= a.indexOf("products"))
  
//     setTimeout(()=>{router.push(`/${b.join('/')}`)},300)
//   }
// },[])







  const [show, setShow] = React.useState(false);
  const anchor = React.useRef(null);
  const handleClick = () => {
    setShow(!show);
  };

  // async function ftch() {
  //   let data = await axiosGet({filter: { urltoken: 'HskQQZN5c9WOIenfb6Hf7xbxJ8rxI12AjOXP9Gkjr5KJ-wuY6DbnTqq19EUOzfjM6j9kjddU_V35R5SIrWPZdg' }})
    // let data = await fetch('https://front.digicod.eu/api/c/?u=LoginRegister&p={filter:{urltoken:params.urltoken,}}')
    // let posts = await data.json()
    // console.log(data);
  // }

  function xor_cypher(input, key) {
    let output = '';
    for (let i = 0; i < input.length; i++) {
        const charCode = input.charCodeAt(i) ^ key.charCodeAt(i % key.length);
        output += String.fromCharCode(charCode);
    }
    return output;
  }

  function xorEncode(txt, pass) {
 
    var ord = []
    var buf = ""
 
    for (z = 1; z <= 255; z++) {ord[String.fromCharCode(z)] = z}
 
    for (j = z = 0; z < txt.length; z++) {
        buf += String.fromCharCode(ord[txt.substr(z, 1)] ^ ord[pass.substr(j, 1)])
        j = (j < pass.length) ? j + 1 : 0
    }
 
    return buf
 
}

  
function xorConvert (text, key) {
  var kL = key.length;

  return Array.prototype
      .slice.call(text)
      .map(function (c, index) {
          return String.fromCharCode(c.charCodeAt(0) ^ key[index % kL].charCodeAt(0));
      }).join('');
}

var key = "mysecretkey";
var txt = "Odysseas78";
var cipherText = xorConvert(txt, key);

// assert(xorConvert(cipherText, key) === txt);

  function encrypt(input, key) {
    const encrypted = xor_cypher(input, key);
    return btoa(encodeURIComponent(encrypted));
  }

 
  function decrypt(encrypted, key) {
    const decoded = atob(encrypted)
    return xor_cypher(decoded, key);
  }


  let enc = new TextEncoder();


function nn(){
  const allbuttons = document.querySelectorAll('button')
  if(allbuttons){
    // console.log(allbuttons[2]?.attributes)
    allbuttons.forEach((f,i)=>{
      f.ontouchstart = (e)=>{
        // console.log(e)
        e.target.style.scale = 0.9
      }
      f.ontouchend = (e)=>{
        e.target.style.scale = 1
      //  return
      }
      // f.onclick = (e)=>{
      //   console.log(e)
      // }
        //   f.touchmove = (e)=>{
        //  console.log(e)
        // }
    
  
    })
  }
}

// nn()



const ss = new Ssr()


  
  
// const [state, action, pending] = useActionState(getUserServer, undefined)

  async function ftch() {
    const res = await fetch('https://front.digicod.eu/api/c/?u=GetBasket&p={}')
    const data = await res.json()
    return data
  }


const handleclc =(e)=>{ 
// axiosGet({})
  // console.log(ftch());
  // const res = getFetch("GetBasket",{})
  // const res = fetch('/next-api/checkout')
  

}
// console.log(state);


  return (

    <div className='z-0'>
      <div>
        <div className='p-[5px]'>
          <div className='flex justify-center text-[2rem] font-semibold' >
            Your shop for digital goods
          </div>
        </div>
        <div className='flex'>
          <div className='flex justify-center w-1/2 p-[5px]' >
            <img src='/media//giftcards.png' />
          </div>
          <div className='flex justify-center w-1/2 p-[5px]' >
            <img src='/media//giftcards.png' />
            <div>

     
    </div>
          </div> 
          <Button 
            {...ss.bc} >{'dataProxy.foo'}</Button>
            <Button className='bg-chart-3' type="submit" onClick={handleclc} >222</Button>  
        
        </div>
        <div>
   
        </div>
      </div>
      <div>
      </div>

       <AvatarIcon className='w-10 h-10' />
  <br/>
      <MoonIcon className='w-10 h-10' />
      <br/>

    </div>

  );
}












