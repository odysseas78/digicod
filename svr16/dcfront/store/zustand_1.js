"use client";
import { nanoid } from 'nanoid';
import { create } from 'zustand';
import { persist, devtools } from 'zustand/middleware'
import { produce } from "immer";


function setNestedImmutable(obj, path, value) {
  if (path.length === 0) return value;

  const [key, ...rest] = path;

  return {
    ...obj,
    [key]: rest.length
      ? setNestedImmutable(obj?.[key] ?? {}, rest, value)
      : value
  };
}

function getNested(obj, path) {
  return path.reduce((acc, key) => acc?.[key], obj);
}

function deleteNestedImmutable(obj, path) {
  if (!path || !path.length) return obj;
  if (obj === null || obj === undefined || typeof obj !== 'object' || Array.isArray(obj)) {
    return obj;
  }
  const [key, ...rest] = path;

  if (!Object.prototype.hasOwnProperty.call(obj, key)) {
    return obj;
  }

  if (rest.length === 0) {
    const keys = Object.keys(obj);
    const newObj = {};
    for (const k of keys) {
      if (k !== key) {
        newObj[k] = obj[k];
      }
    }
    return newObj;
  }

  const deletedValue = deleteNestedImmutable(obj[key], rest);
  if (deletedValue === obj[key]) {
    return obj;
  }
  return {
    ...obj,
    [key]: deletedValue
  };
}

export const simpleStore = create(devtools((set, get) => ({
  cset:(d)=>set((prev)=>{
    const ff = {...prev}
    return {...ff, ...d}
  }),
  get: get,
  set:set,

  pset: (arg1, arg2) =>
    set((prev) => {
      let path, value;

      if (typeof arg1 === "function") {
        const res = arg1(prev);
        path = res.path;
        value = res.value;
      } else {
        path = arg1;
        value = arg2;
      }

      return setNestedImmutable(prev, path, value);
    }),

  pget: (pathOrFn) => {
    const state = get();
    const path =
      typeof pathOrFn === "function"
        ? pathOrFn(state)
        : pathOrFn;

    return getNested(state, path);
  },

  pdelete: (pathOrFn) =>
    set((prev) => {
      const path =
        typeof pathOrFn === "function"
          ? pathOrFn(prev)
          : pathOrFn;

      if (!path || !Array.isArray(path) || path.length === 0) {
        return prev;
      }

      const result = deleteNestedImmutable(prev, path);
      return result;
    }, true),

  allertdialog:[],
  removedialog:(id) => set((prev) => {
     return { allertdialog: prev.allertdialog.filter((d, i) => i !== id) } }),
  setdialog:(d) => set((prev) => { return { allertdialog: [...prev.allertdialog, d] } }),




}), { name: 'simpleStore' }))



export const perStore = create(devtools(persist((set, get) => ({
  cset:(d)=>set((prev)=>{
    const ff = {...prev}
    return {...ff, ...d}
  }),

  coinwallet: {
    walletData: 0,
    loading: false
  },


}), { name: 'perStore' })))




export const useFilter = create((set => ({
  filter: 'all',
  ddd:'kkk',
  setFilter: (value) => set({ filter: value })
})))



export const defStore = create(devtools(persist((set, get) => ({

  scrollste:null,
  Set:(data) => {
    set((prev)=>{
      return {...prev,...data}})
  },


  user:null,

  dset: (arg1, arg2) =>
    set((prev) => {
      let path, value;

      if (typeof arg1 === "function") {
        const res = arg1(prev);
        path = res.path;
        value = res.value;
      } else {
        path = arg1;
        value = arg2;
      }

      return setNestedImmutable(prev, path, value);
    }),

  dget: (pathOrFn) => {
    const state = get();
    const path =
      typeof pathOrFn === "function"
        ? pathOrFn(state)
        : pathOrFn;

    return getNested(state, path);
  },

  ddelete: (pathOrFn) =>
    set((prev) => {
      const path =
        typeof pathOrFn === "function"
          ? pathOrFn(prev)
          : pathOrFn;

      if (!path || !Array.isArray(path) || path.length === 0) {
        return prev;
      }

      const result = deleteNestedImmutable(prev, path);
      return result;
    }, true),
}), { name: 'defStore' })))