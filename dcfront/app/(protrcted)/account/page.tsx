import { cookies, headers } from "next/headers";
import { redirect } from 'next/navigation'
import Account from './Account';
import fetchActionServer from '@/app/actions/fetchActionServer';


interface PageProps {
  params: { catslug?: string };
  searchParams: { [key: string]: string | string[] | undefined };
}

export default async function AccountPage({ params, searchParams }: PageProps) {
  // const prams = await params
  // const sprams = await searchParams
  // const cookieStore = await cookies()
  // await new Promise(resolve => setTimeout(resolve, 5000)); s
  // console.log("LoginPage props:", formdata);
 
  

    // const orders = (sprams.c === 'orders') && await fetchActionServer('GetOrder', {})
    // const coinWallet = (sprams.c === 'wallet') && await fetchActionServer('GetCoinWallet', {})

  return (
    <div>
     <Account {...{ }} />
    </div>
  ) 
}