"use server"
import SiteHeader from './SiteHeader'
import Cart from "@/app/checkout/cart/cart";
import CurrSel from "@/components/Currency/CurrencyDropdown";




export default async function SiteHeaderServer({ fbasket, fcategory, fcurrency }) {
"use server"



  
  
  return (
   <SiteHeader {...{ fbasket, fcategory, fcurrency }} />
  )
}


