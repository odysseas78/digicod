"use client";
import { nanoid } from 'nanoid';
import { create } from 'zustand';
import { persist, devtools } from 'zustand/middleware'




export const headStore = create(devtools(persist((set, get) => ({
  cset:(d)=>set((prev)=>{
    const ff = {...prev}
    return {...ff, ...d}
  }),

  theme:'dark',

}), { name: 'headStore' })))







// #######################################################################


