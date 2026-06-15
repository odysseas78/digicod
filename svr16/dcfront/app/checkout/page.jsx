"use server"
import { use } from 'react';
import fetchActionServer from '@/app/actions/fetchActionServer';
// import Getbasket from '@/app/actions/cart';
import dynamic from 'next/dynamic';
import { Suspense } from "react";
import { NextResponse } from 'next/server';
import { NextRequest } from 'next/server';
import { cookies, headers } from "next/headers";
// const Checkout = dynamic(() => import('@/app/checkout/Checkout'));
// import CheckoutServer from '@/app/checkout/CheckoutServer';
// import BrandList from '../page';
// import useAxiosFunction from '@/hooks/useAxiosFunctionServer';
import Checkout from '@/app/checkout/Checkout';



const delay = (time) => new Promise((resolve) => {
  setTimeout(resolve, time);
});
async function CheckoutP({params, searchParams}) {
  
  //   const cookieStore = await cookies();
  //   const headerStore = await headers();
  //       console.log()
  //  const Data = await fetchActionServer("GetBasket", {})
  //   const data = Data;
  
  return (
    // <Suspense fallback={<div className='z-50'>Loading...</div>} >
      <Checkout  />
      // <Checkout basketdata={data} />
    // </Suspense >
  )
};

export default CheckoutP;
