"use client";

import { signal } from '@preact/signals-react';
import wk from '@/lib/wk';


// Funktion zur Erstellung eines Proxy, der neue Eigenschaften als Signale speichert
function createSignalProxy(target) {
  return new Proxy(target, {
    set(obj, prop, value) {
      const store = wk.defSte();
      store.Set({[obj[prop]]:value})
      // Bedingung: Hier können Sie Ihre spezifischen Bedingungen prüfen
      // Beispiel: Alle neuen Werte werden in Signale umgewandelt
      obj[prop] += value
      return true; // Indiziert, dass das Set erfolgreich war
    },
    get(obj, prop) {
      const store = wk.defSte();
      return store.get()[obj[prop]]
    }
  });
}

// Verwendung des Proxies
export const sobj = createSignalProxy({});



// manager.addProperty('key1', 456);