"use client"
import React from 'react'
import { simpleStore } from "@/store/zustand_1";




export default function Dialogs(){
   const simste = simpleStore()

   return (
      simste.pget(["simpldialogs"]) &&
      Object.keys(simste.pget(["simpldialogs"])).map((k)=>{
          return (
              <div className="fixed" key={k}>
                  {simste.pget(["simpldialogs"])[k]}
              </div>
          )
      })
   )
}