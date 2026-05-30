  // ############################################
  export function mergeUniqueKeys<T extends Record<string, any>>(target: T, source: Record<string, any>): T {
   const seenKeys = new Set<string>();
   function recursiveMerge(target: any, source: any) {
     if (typeof source !== "object" || source === null) {
       return;
     }
     for (const key in source) {
       if (key in target && !seenKeys.has(key)) {
         target[key] = source[key];
         seenKeys.add(key);
       }
       if (typeof source[key] === "object" && source[key] !== null) {
         recursiveMerge(target, source[key]);
       }
     }
   }
   recursiveMerge(target, source);
   return target;
 }
 // #########################################################
//  export function getCookie(name=null) {
//   if (typeof document === 'undefined') return null;
//   if(!name) return document.cookie;
//     return document.cookie.split('; ').find(row => row.startsWith(name + '='))?.split('=')[1]
// }

export function currencyFormat(amount:any, cursign:any){
  
  const formatted = new Intl.NumberFormat("de-DE", {
    style: "currency",
    currency: cursign,
  }).format(amount)
  return formatted
}