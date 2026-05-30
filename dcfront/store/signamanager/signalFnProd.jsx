"use client";
import { createContext } from "react";
// import useAxiosFunction from "@/hooks/useAxiosFunction";
import { signal, useSignal, Signal } from '@preact/signals-react';


// Funktion zur Erstellung eines Proxy, der neue Eigenschaften als Signale speichert
function createSignalProxy(target) {
  const s =(value)=> new Signal(value)
  return new Proxy(target, {
    
    set(obj, prop, value) {
      
        if(!obj[prop]) obj[prop] = s(value)
   
      // Bedingung: Hier können Sie Ihre spezifischen Bedingungen prüfen
      // Beispiel: Alle neuen Werte werden in Signale umgewandelt
      
      return true; // Indiziert, dass das Set erfolgreich war
    },
    get(obj, prop) {

      return obj[prop]
    }
  });
}

// Verwendung des Proxies
export const sobj = createSignalProxy({});

