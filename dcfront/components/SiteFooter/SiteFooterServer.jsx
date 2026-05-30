"use server";
import dynamic from 'next/dynamic'
import { Suspense } from "react";
// const SiteFooter = dynamic(() => import('./SiteFooter'));
import SiteFooter from '@/components/SiteFooter/SiteFooter'


export default async function SiteFooterServer() {


    return (
        <>
        {/* <Suspense fallback={null}> */}
            <SiteFooter  />
            {/* </Suspense> */}
        </>
    )
}



