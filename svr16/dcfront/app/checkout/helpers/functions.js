import syncFingerprintCookie from "@/app/actions/syncFingerprintCookie";
import { getBrowserFingerprint } from "@/app/lib/fingerprint-client";

export function toggleAnim(refo) {
   const d = refo.collapsbasket.current?.classList.contains('grid-rows-[1fr]')
   const icon = refo.chevicon.current?.classList
   const body = refo.collapsbasket.current?.classList
   const close = () => {
     body['add'](['grid-rows-[0fr]'])
     body['remove'](['grid-rows-[1fr]'])
     icon['add'](['rotate-0'])
     icon['remove'](['rotate-180'])
   }
   const open = () => {
     body['add'](['grid-rows-[1fr]'])
     body['remove'](['grid-rows-[0fr]'])
 
     icon['add'](['rotate-180'])
     icon['remove'](['rotate-0'])
   }
   if (d) {
     close()
   } else {
     open()
   }
 }
 
 
 // ###########################################################################
// function initIndexedDB(dbName, storeName) {
 //   return new Promise((resolve, reject) => {
 //       const request = indexedDB.open(dbName, 1); // Version 1
 
 //       request.onupgradeneeded = (event) => {
 //           const db = event.target.result;
 //           if (!db.objectStoreNames.contains(storeName)) {
 //               db.createObjectStore(storeName);
 //           }
 //       };
 
 //       request.onsuccess = () => resolve(request.result);
 //       request.onerror = () => reject("IndexedDB konnte nicht geöffnet werden");
 //   });
 // }
 
 
 // initIndexedDB("DeviceDB", "Fingerprints")
 
 // // 🌟 SPEICHERUNG IN INDEXEDDB 🌟
 // function saveToIndexedDB(dbName, storeName, key, value) {
 //     return new Promise((resolve, reject) => {
 //         const request = indexedDB.open(dbName, 1);
 //         request.onerror = () => reject("IndexedDB error");
 //         request.onsuccess = () => {
 //             const db = request.result;
 //             const tx = db.transaction(storeName, "readwrite");
 //             const store = tx.objectStore(storeName);
 //             store.put(value, key);
 //             tx.oncomplete = () => resolve();
 //             tx.onerror = () => reject("Transaction failed");
 //         };
 //         request.onupgradeneeded = (event) => {
 //             event.target.result.createObjectStore(storeName);
 //         };
 //     });
 // }
 
 // function getFromIndexedDB(dbName, storeName, key) {
 //     return new Promise((resolve, reject) => {
 //         const request = indexedDB.open(dbName, 1);
 //         request.onerror = () => reject("IndexedDB error");
 //         request.onsuccess = () => {
 //             const db = request.result;
 //             const tx = db.transaction(storeName, "readonly");
 //             const store = tx.objectStore(storeName);
 //             const getRequest = store.get(key);
 //             getRequest.onsuccess = () => resolve(getRequest.result);
 //             getRequest.onerror = () => reject("Get request failed");
 //         };
 //     });
 // }
 
 // 🌟 SENDEN AN SERVER 🌟
 async function sendFingerprintToServer(fingerprint) {
     try {
         const response = await fetch("https://yourserver.com/api/fingerprint", {
             method: "POST",
             headers: {
                 "Content-Type": "application/json",
             },
             body: JSON.stringify({ fingerprint }),
         });
         return response.ok;
     } catch (error) {
         console.error("Server error:", error);
         return false;
     }
 }
 
 // 🌟 GESAMTE FUNKTION 🌟
export async function initFingerprint() {
  "use client";
  if(typeof document !== 'undefined'){
    const fingerprint = await getBrowserFingerprint();
    await syncFingerprintCookie(fingerprint);
  }
 }
 // ####################################################################################

 export function currencyFormat(amount, currency){
    const formatted = new Intl.NumberFormat("de-DE", {
      style: "currency",
      currency: currency,
    }).format(amount)
    return formatted
  }
