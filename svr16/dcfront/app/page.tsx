import Homepage from '@/app/Homepage/Homepage'
import fetchActionServer from '@/app/actions/fetchActionServer';
import { cookies, headers } from "next/headers";
import { BrandGrid } from './brandGrid'
import fs from 'node:fs';
import { createClient } from "redis";






// import Link from 'next/link';


// console.log('rootpage_0')



interface PageProps {
  params: { catslug?: string };
  searchParams: { [key: string]: string | string[] | undefined };
}

export default async function Page({ params, searchParams }: PageProps) {
  const cookieStore = await cookies();
  const headerStore = await headers();
  const { catslug } = await params;


  // const v = await client.get("testkey");
  // !v && await client.set("testkey", "testvalue");
  // const client = await createClient({
  //   url: "redis://127.0.0.1:6379"
  // })
  //   .on("error", (err) => console.log("Redis Client Error", err))
  //   .connect();
  // const value = await client.get("testkey");

  // value && client.destroy();



//    const Dcft = <div className='flex flex-row flex-wrap justify-center' >
//    {
//      data.filter((d:any)=>d.image2).map((b:any)=>{
 
//        return (
//          <div key={b.id}>
//             <BrandGrid {...{b}} />
                  
//          </div>
        
//        )
//      })
//    }
//  </div>
// console.log(data[0].title)
return (
      <Homepage {...{ }} />
)
}


