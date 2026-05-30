import { clsx, type ClassValue } from "clsx"
import { WithImplicitCoercion } from "node:buffer";
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
export const delay = (time:any) => new Promise((resolve) => {
  setTimeout(resolve, time);
});

export function dateFormat (date: string | number | Date, dateonly=""){
   const doptions = {
     year: "2-digit",
     month:"2-digit",
     day:"2-digit",
     }
     const toptions = {
       hour12 : false,
       hour:  "2-digit",
       minute: "2-digit",
     }
     //@ts-ignore
   const dres = new Date(date).toLocaleDateString("de-DE", doptions);
   //@ts-ignore
   const tres = new Date(date).toLocaleTimeString("de-DE", toptions);
   
   if(dateonly === "dateonly"){
     return (`${dres}`)
   } else {
     return (`${dres} ${tres}`)
   }
 }


export function currencyFormat(amount:any, currency:any){
   const formatted = new Intl.NumberFormat("de-DE", {
     style: "currency",
     currency: currency,
   }).format(amount)
   return formatted
 }


export function generatePassword(length:any, upper=true, lower=true, num=null,sonder=null) {
  var result = '';
  
  var upper1 = upper ? 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':''
  var lower1 = lower ? 'abcdefghijklmnopqrstuvwxyz':''
  var num1 = num ? '0123456789':''
  var sonder1 = sonder ? '!@#$%^&*()':''
  var characters = upper1+lower1+num1+sonder1
  var charactersLength = characters.length;
  for (var i = 0; i < length; i++) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
  }
  return result;
}

function ClsListToggle(el:any, clsList:any) {
   
   for (const cls of clsList){
      el?.classList.toggle(cls)
   }
}



export const generateId = () => (
    Math.random().toString(16).slice(2) + new Date().getTime().toString(36)
);



function xorCipher(inputString: string, key: string) {
  let encrypted = "";

  for (let i = 0; i < inputString.length; i++) {
    const charCode = inputString.charCodeAt(i);
    const keyCode = key.charCodeAt(i % key.length);
    encrypted += String.fromCharCode(charCode ^ keyCode);
  }

  return encrypted;
}

function encrypt(inputString: string, key: string) {
  const encrypted = xorCipher(inputString, key);
  return Buffer.from(encrypted, "utf-8").toString("base64");
}

function decrypt(encryptedString: WithImplicitCoercion<string>, key: string) {
  const encrypted = Buffer.from(encryptedString, "base64").toString("utf-8");
  return xorCipher(encrypted, key);
}


export function getCookies(name:any) {
    if (typeof document === 'undefined') return null;
    if(!name) return document.cookie;
      return document.cookie.split('; ').find(row => row.startsWith(name + '='))?.split('=')[1]
  }

export function setCookie(name: any, value: any, days = 365) {
  const expires = new Date(Date.now() + days * 864e5).toUTCString();
  document.cookie = `${name}=${value}; expires=${expires}; path=/; SameSite=Lax`;
}